from __future__ import annotations

import ast
import typing

import unimport.constants as C
from unimport import utils
from unimport.analyzers.decarators import generic_visit, skip_import
from unimport.analyzers.importable import ImportableNameAnalyzer, SuggestionNameAnalyzer
from unimport.analyzers.utils import set_tree_parents
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("ImportAnalyzer",)


class ImportAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "source",
        "include_star_import",
        "defined_names",
        "any_import_error",
        "if_dispatch_names",
        "_in_type_checking",
    )

    IGNORE_MODULES_IMPORTS = ("__future__",)
    IGNORE_IMPORT_NAMES = ("__all__", "__doc__", "__name__")

    def __init__(
        self, *, source: str, include_star_import: bool = False, defined_names: set[str] | None = None
    ) -> None:
        self.source = source
        self.include_star_import = include_star_import
        self.defined_names = defined_names or set()

        self.any_import_error = False

        # Names imported in both the body and the else branch of each enclosing ``if`` (version/platform dispatch).
        self.if_dispatch_names: list[set[str]] = []
        self._in_type_checking: bool = False

    def traverse(self, tree) -> None:
        self.visit(tree)

    def visit_def(self, node):
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_ClassDef = visit_FunctionDef = visit_AsyncFunctionDef = visit_def

    @generic_visit
    @skip_import
    def visit_Import(self, node: ast.Import) -> None:
        for column, alias in enumerate(node.names):
            name = alias.asname or alias.name
            if self.is_explicit_reexport(alias):
                continue
            if name in self.IGNORE_IMPORT_NAMES or self.is_if_dispatch(name):
                continue

            Import.register(
                lineno=node.lineno,
                column=column + 1,
                name=name,
                package=alias.name,
                node=node,
                is_type_checking=self._in_type_checking,
            )

    @generic_visit
    @skip_import
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        is_star = node.names[0].name == "*"

        for column, alias in enumerate(node.names):
            package = "." * node.level + (node.module or "")  # `from . import x` has no module
            if (package in self.IGNORE_MODULES_IMPORTS) or (is_star and not self.include_star_import):
                return

            name = package if is_star else (alias.asname or alias.name)
            if self.is_explicit_reexport(alias):
                continue
            if name in self.IGNORE_IMPORT_NAMES or self.is_if_dispatch(name):
                continue

            ImportFrom.register(
                lineno=node.lineno,
                column=column + 1,
                name=name,
                package=package,
                star=is_star,
                suggestions=self.get_suggestions(package) if is_star else [],
                node=node,
                is_type_checking=self._in_type_checking,
            )

    @staticmethod
    def is_explicit_reexport(alias: ast.alias) -> bool:
        """``import X as X`` and ``from m import X as X`` mark an explicit re-export (PEP 484)."""
        return alias.asname is not None and alias.asname == alias.name

    @staticmethod
    def _is_type_checking_block(if_node: ast.If) -> bool:
        test = if_node.test
        if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
            return True
        if isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING":
            return True
        return False

    @staticmethod
    def _collect_import_names(nodes: list[ast.stmt], *, recursive: bool = True) -> set[str]:
        names: set[str] = set()
        for node in nodes:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    names.add(alias.asname or alias.name)
            elif recursive and isinstance(node, ast.If):
                names |= ImportAnalyzer._collect_import_names(node.body)
                names |= ImportAnalyzer._collect_import_names(node.orelse)
        return names

    @staticmethod
    def _collect_assigned_names(nodes: list[ast.stmt]) -> set[str]:
        """Names assigned directly in a branch (``x = None``), following an ``elif`` chain."""
        names: set[str] = set()
        for node in nodes:
            if isinstance(node, ast.Assign):
                names.update(target.id for target in node.targets if isinstance(target, ast.Name))
            elif isinstance(node, ast.AnnAssign) and node.value is not None and isinstance(node.target, ast.Name):
                names.add(node.target.id)
        if len(nodes) == 1 and isinstance(nodes[0], ast.If):  # elif
            names |= ImportAnalyzer._collect_assigned_names(nodes[0].body)
            names |= ImportAnalyzer._collect_assigned_names(nodes[0].orelse)
        return names

    def visit_If(self, if_node: ast.If) -> None:
        if self._is_type_checking_block(if_node):
            self._in_type_checking = True
            for node in if_node.body:
                self.visit(node)
            self._in_type_checking = False
            for node in if_node.orelse:
                self.visit(node)
            return

        if_names = self._collect_import_names(if_node.body)
        orelse_names = self._collect_import_names(if_node.orelse, recursive=False)
        # ``if ...: import tomllib`` / ``else: tomllib = None``: a fallback binding, not a reassignment.
        if_assigned = self._collect_assigned_names(if_node.body)
        orelse_assigned = self._collect_assigned_names(if_node.orelse)

        self.if_dispatch_names.append(
            (if_names & orelse_names) | (if_names & orelse_assigned) | (if_assigned & orelse_names)
        )
        try:
            self.generic_visit(if_node)
        finally:
            self.if_dispatch_names.pop()

    def is_if_dispatch(self, name: str) -> bool:
        return any(name in names for names in self.if_dispatch_names)

    def visit_Try(self, node: ast.Try) -> None:
        # Imports guarded by an except handler are usually optional-dependency fallbacks, so they are left alone.
        # try/finally without a handler guards nothing. Restore the previous value so a nested try does not
        # clear the enclosing one's state.
        previous = self.any_import_error
        self.any_import_error = previous or bool(node.handlers)
        try:
            self.generic_visit(node)
        finally:
            self.any_import_error = previous

    def visit_TryStar(self, node: ast.AST) -> None:
        # try / except* (Python 3.11+). ast.TryStar does not exist before 3.11, hence the broad annotation.
        self.visit_Try(node)  # type: ignore[arg-type]

    @classmethod
    def iget_importable_name(cls, package: str) -> typing.Iterator[str]:
        if utils.is_std(package):
            yield from utils.get_module_dir(package)

        elif source := utils.get_source(package):
            try:
                tree = ast.parse(source)
            except SyntaxError:
                pass
            else:
                importable_name_analyzer = ImportableNameAnalyzer()
                importable_name_analyzer.traverse(tree)
                if importable_name_analyzer.importable_nodes:
                    for node in importable_name_analyzer.importable_nodes:
                        if isinstance(node.value, str):
                            yield node.value
                else:
                    suggestion_name_analyzer = SuggestionNameAnalyzer()
                    set_tree_parents(tree)
                    suggestion_name_analyzer.traverse(tree)
                    for node in suggestion_name_analyzer.suggestions_nodes:  # type: ignore[assignment]
                        if isinstance(node, ast.Name):
                            yield node.id
                        elif isinstance(node, ast.alias):
                            yield node.asname or node.name
                        elif isinstance(node, C.DEF_TUPLE):
                            yield node.name

    def get_suggestions(self, package: str) -> list[str]:
        names = set(map(lambda name: name.name.split(".")[0], Name.names))
        from_names = self.iget_importable_name(package)
        return sorted(set(from_names) & (names - self.defined_names))
