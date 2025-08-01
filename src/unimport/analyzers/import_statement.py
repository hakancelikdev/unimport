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
        "if_names",
        "orelse_names",
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

        self.if_names: set[str] = set()
        self.orelse_names: set[str] = set()

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
            if name in self.IGNORE_IMPORT_NAMES or (name in self.if_names and name in self.orelse_names):
                continue

            Import.register(lineno=node.lineno, column=column + 1, name=name, package=alias.name, node=node)

    @generic_visit
    @skip_import
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        is_star = node.names[0].name == "*"

        for column, alias in enumerate(node.names):
            package = node.module if not node.level else "." * node.level + str(node.module) or ""
            if (package in self.IGNORE_MODULES_IMPORTS) or (is_star and not self.include_star_import):
                return

            name = package if is_star else (alias.asname or alias.name)
            if name in self.IGNORE_IMPORT_NAMES or (name in self.if_names and name in self.orelse_names):
                continue

            ImportFrom.register(
                lineno=node.lineno,
                column=column + 1,
                name=name,
                package=package,
                star=is_star,
                suggestions=self.get_suggestions(package) if is_star else [],
                node=node,
            )

    def visit_If(self, if_node: ast.If) -> None:
        self.if_names = {
            name.asname or name.name
            for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.body)
            for name in n.names  # type: ignore
        }

        self.orelse_names = {
            name.asname or name.name
            for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.orelse)
            for name in n.names  # type: ignore
        }

        self.generic_visit(if_node)

        self.if_names = set()
        self.orelse_names = set()

    def visit_Try(self, node: ast.Try) -> None:
        self.any_import_error = True

        self.generic_visit(node)

        self.any_import_error = False

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
