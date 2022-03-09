"""This module performs static analysis using AST on the python code that's
given as a string and reports its findings."""

import ast
import functools
import re
from pathlib import Path
from typing import FrozenSet, List, Set, cast

from unimport import color
from unimport import constants as C
from unimport import utils
from unimport.relate import first_occurrence, get_parents, relate
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("Analyzer",)


def _generic_visit(func: C.FunctionT) -> C.FunctionT:
    """decorator to make visitor work _generic_visit."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        obj = args[0]
        node = args[1]
        obj.generic_visit(node)

    return cast(C.FunctionT, wrapper)


class _DefinedNameAnalyzer(ast.NodeVisitor):
    __slots__ = ("defined_names",)

    def __init__(self):
        self.defined_names: Set[str] = set()

    @_generic_visit
    def visit_FunctionDef(self, node: C.ASTFunctionT) -> None:
        self.defined_names.add(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    @_generic_visit
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.defined_names.add(node.name)

    @_generic_visit
    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)


class _ImportAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "source",
        "include_star_import",
        "any_import_error",
        "defined_names",
    )

    ignore_modules_imports = ("__future__",)
    skip_import_comments_regex = "#.*(unimport: {0,1}skip|noqa)"

    def __init__(
        self,
        *,
        source: str,
        include_star_import: bool = False,
    ):
        self.source = source
        self.include_star_import = include_star_import

        self.any_import_error = False
        self.defined_names: Set[str] = set()

    def traverse(self, tree) -> None:
        defined_name_scanner = _DefinedNameAnalyzer()
        defined_name_scanner.visit(tree)
        self.defined_names = defined_name_scanner.defined_names

        self.visit(tree)

    def visit_ClassDef(self, node) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    def visit_FunctionDef(self, node: C.ASTFunctionT) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    @_generic_visit
    def visit_Import(self, node: ast.Import) -> None:
        if self.skip_import(node):
            return None

        for column, alias in enumerate(node.names):
            Import.register(
                lineno=node.lineno,
                column=column + 1,
                name=(alias.asname or alias.name),
                package=alias.name,
                node=node,
            )

    @_generic_visit
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if self.skip_import(node):
            return None

        is_star = node.names[0].name == "*"
        for column, alias in enumerate(node.names):
            if not node.level:
                package = node.module
            else:
                package = "." * node.level + str(node.module) or ""
            alias_name = alias.asname or alias.name
            if (package in self.ignore_modules_imports) or (
                is_star and not self.include_star_import
            ):
                return
            ImportFrom.register(
                lineno=node.lineno,
                column=column + 1,
                name=package if is_star else alias_name,
                star=is_star,
                suggestions=self.get_suggestions(package) if is_star else [],
                package=package,
                node=node,
            )

    def visit_Try(self, node: ast.Try) -> None:
        self.any_import_error = True

        self.generic_visit(node)

        self.any_import_error = False

    def skip_import(self, node: C.ASTImport) -> bool:
        if C.PY38_PLUS:
            source_segment = "\n".join(
                self.source.splitlines()[node.lineno - 1 : node.end_lineno]
            )
        else:
            source_segment = self.source.splitlines()[node.lineno - 1]
        return (
            bool(
                re.search(
                    self.skip_import_comments_regex,
                    source_segment,
                    re.IGNORECASE,
                )
            )
            or self.any_import_error
        )

    def get_suggestions(self, package: str) -> List[str]:
        names = set(map(lambda name: name.name.split(".")[0], Name.names))
        from_names = _ImportableAnalyzer.get_names(package)
        return sorted(from_names & (names - self.defined_names))


class _NameAnalyzer(ast.NodeVisitor):
    def visit_ClassDef(self, node) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    def visit_FunctionDef(self, node: C.ASTFunctionT) -> None:
        Scope.add_current_scope(node)

        self._type_comment(node)
        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_str_helper(self, value: str, node: ast.AST) -> None:
        parent = first_occurrence(node, *C.ASTFunctionTuple)
        is_annassign_or_arg = any(
            isinstance(parent, (ast.AnnAssign, ast.arg))
            for parent in get_parents(node)
        )
        if is_annassign_or_arg or (
            parent is not None and parent.returns is node
        ):
            self.join_visit(value, node)

    def visit_Str(self, node: ast.Str) -> None:
        self.visit_str_helper(node.s, node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str):
            self.visit_str_helper(node.value, node)

    @_generic_visit
    def visit_Name(self, node: ast.Name) -> None:
        if not isinstance(node.parent, ast.Attribute):  # type: ignore
            Name.register(lineno=node.lineno, name=node.id, node=node)

    @_generic_visit
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if not isinstance(node.value, ast.Call):
            names = []
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Attribute):
                    names.append(sub_node.attr)
                elif isinstance(sub_node, ast.Name):
                    names.append(sub_node.id)
            names.reverse()
            Name.register(lineno=node.lineno, name=".".join(names), node=node)

    @_generic_visit
    def visit_Assign(self, node: ast.Assign) -> None:
        self._type_comment(node)

    @_generic_visit
    def visit_arg(self, node: ast.arg) -> None:
        self._type_comment(node)

    @_generic_visit
    def visit_Subscript(self, node: ast.Subscript) -> None:
        # type_variable
        # type_var = List["object"] etc.

        def visit_constant_str(node: C.ASTNameType) -> None:
            """Separates the value by node type (str or constant) and gives it
            to the visit function."""

            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                self.join_visit(node.value, node)
            elif isinstance(node, ast.Str):
                self.join_visit(node.s, node)

        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "typing"
        ) or (
            isinstance(node.value, ast.Name)
            and node.value.id in C.SUBSCRIPT_TYPE_VARIABLE
        ):

            if C.PY39_PLUS:
                _slice = node.slice
            else:
                _slice = node.slice.value  # type: ignore

            if isinstance(_slice, ast.Tuple):  # type: ignore
                for elt in _slice.elts:  # type: ignore
                    if isinstance(elt, (ast.Constant, ast.Str)):
                        visit_constant_str(elt)
            else:
                if isinstance(_slice, (ast.Constant, ast.Str)):  # type: ignore
                    visit_constant_str(_slice)  # type: ignore

    @_generic_visit
    def visit_Call(self, node: ast.Call) -> None:
        # type_variable
        # cast("type", return_value)
        if (
            (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "typing"
                and node.func.attr == "cast"
            )
            or isinstance(node.func, ast.Name)
            and node.func.id == "cast"
        ):
            if isinstance(node.args[0], ast.Constant) and isinstance(
                node.args[0].value, str
            ):
                self.join_visit(node.args[0].value, node.args[0])
            elif isinstance(node.args[0], ast.Str):
                self.join_visit(node.args[0].s, node.args[0])

    def _type_comment(self, node: ast.AST) -> None:
        if isinstance(node, C.ASTFunctionTuple):
            mode = "func_type"
        else:
            mode = "eval"
        type_comment = getattr(node, "type_comment", None)
        if type_comment is not None:
            self.join_visit(type_comment, node, mode=mode)

    def join_visit(
        self, value: str, node: ast.AST, *, mode: str = "eval"
    ) -> None:
        """A function that parses the value, copies locations from the node and
        includes them in self.visit."""
        try:
            if C.PY38_PLUS:
                tree = ast.parse(value, mode=mode, type_comments=True)
            else:
                tree = ast.parse(value, mode=mode)
        except SyntaxError:
            return None
        else:
            relate(tree, parent=node.parent)  # type: ignore
            for new_node in ast.walk(tree):
                ast.copy_location(new_node, node)
            self.visit(tree)


class _ImportableAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "importable_nodes",
        "suggestions_nodes",
    )

    def __init__(self) -> None:
        self.importable_nodes: List[
            C.ASTNameType
        ] = []  # nodes on the __all__ list
        self.suggestions_nodes: List[C.ASTImportableT] = []  # nodes on the CFN

    def visit_CFN(self, node: C.CFNT) -> None:
        Scope.add_current_scope(node)

        if not first_occurrence(node, C.DefTuple):
            self.suggestions_nodes.append(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_ClassDef = visit_CFN
    visit_FunctionDef = visit_CFN
    visit_AsyncFunctionDef = visit_CFN

    @_generic_visit
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.suggestions_nodes.append(alias)

    @_generic_visit
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if not node.names[0].name == "*":
            for alias in node.names:
                self.suggestions_nodes.append(alias)

    @_generic_visit
    def visit_Assign(self, node: ast.Assign) -> None:
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(
            node.value, (ast.List, ast.Tuple, ast.Set)
        ):
            for item in node.value.elts:
                if isinstance(item, (ast.Constant, ast.Str)):
                    self.importable_nodes.append(item)

        for target in node.targets:  # we only get assigned names
            if isinstance(target, (ast.Name, ast.Attribute)):
                self.suggestions_nodes.append(target)

    @_generic_visit
    def visit_Expr(self, node: ast.Expr) -> None:
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and isinstance(node.value.func.value, ast.Name)
            and node.value.func.value.id == "__all__"
        ):
            if node.value.func.attr == "append":
                for arg in node.value.args:
                    if isinstance(arg, (ast.Constant, ast.Str)):
                        self.importable_nodes.append(arg)

            elif node.value.func.attr == "extend":
                for arg in node.value.args:
                    if isinstance(arg, ast.List):
                        for item in arg.elts:
                            if isinstance(item, (ast.Constant, ast.Str)):
                                self.importable_nodes.append(item)

    @classmethod
    def get_names(cls, package: str) -> FrozenSet[str]:
        if utils.is_std(package):
            return utils.get_dir(package)

        source = utils.get_source(package)
        if source:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                return frozenset()
            else:
                visitor = cls()
                relate(tree)
                visitor.visit(tree)
                return visitor.get_all() or visitor.get_suggestion()
        return frozenset()

    def get_all(self) -> FrozenSet[str]:
        names = set()
        for node in self.importable_nodes:
            if isinstance(node, ast.Constant):
                names.add(node.value)
            elif isinstance(node, ast.Str):
                names.add(node.s)
        return frozenset(names)

    def get_suggestion(self) -> FrozenSet[str]:
        names = set()
        for node in self.suggestions_nodes:  # type: ignore
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.alias):
                names.add(node.asname or node.name)
            elif isinstance(node, C.DefTuple):
                names.add(node.name)
        return frozenset(names)

    def clear(self):
        self.importable_nodes.clear()
        self.suggestions_nodes.clear()


class Analyzer(ast.NodeVisitor):
    __slots__ = ("source", "path", "include_star_import")

    skip_file_regex = "#.*(unimport: {0,1}skip_file)"

    def __init__(
        self,
        *,
        source: str,
        path: Path = Path("<unknown file>"),
        include_star_import: bool = False,
    ):
        self.source = source
        self.path = path
        self.include_star_import = include_star_import

    def __enter__(self):
        self.traverse()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.clear()

    def traverse(self) -> None:
        if self.skip_file():
            return None

        try:
            if C.PY38_PLUS:
                tree = ast.parse(self.source, type_comments=True)
            else:
                tree = ast.parse(self.source)
        except SyntaxError as e:
            print(
                color.paint(str(e), color.RED)
                + " at "
                + color.paint(self.path.as_posix(), color.GREEN)
            )
            return None

        """
        Set parent
        """
        relate(tree)

        Scope.add_global_scope(tree)

        """
        Name analyzer
        """
        _NameAnalyzer().visit(tree)
        """
        Receive items on the __all__ list
        """
        importable_visitor = _ImportableAnalyzer()
        importable_visitor.visit(tree)
        for node in importable_visitor.importable_nodes:
            if isinstance(node, ast.Constant):
                Name.register(
                    lineno=node.lineno,
                    name=str(node.value),
                    node=node,
                    is_all=True,
                )
            elif isinstance(node, ast.Str):
                Name.register(
                    lineno=node.lineno, name=node.s, node=node, is_all=True
                )
        importable_visitor.clear()
        """
        Import analyzer
        """
        _ImportAnalyzer(
            source=self.source,
            include_star_import=self.include_star_import,
        ).traverse(tree)

        Scope.remove_current_scope()

    def skip_file(self) -> bool:
        return bool(
            re.search(self.skip_file_regex, self.source, re.IGNORECASE)
        )

    @staticmethod
    def clear():
        Name.clear()
        Import.clear()
        ImportFrom.clear()
        Scope.clear()
