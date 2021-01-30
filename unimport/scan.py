"""This module performs static analysis using AST on the python code that's
given as a string and reports its findings."""
import ast
import functools
import re
from pathlib import Path
from typing import FrozenSet, Iterator, List, Set, Union, cast

from unimport import color
from unimport import constants as C
from unimport import utils
from unimport.relate import first_occurrence, get_parents, relate
from unimport.statement import Import, ImportFrom, Name

__all__ = ["Scanner"]


def recursive(func: C.Function) -> C.Function:
    """decorator to make visitor work recursive."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.generic_visit(*args)

    return cast(C.Function, wrapper)


class _DefinedNameScanner(ast.NodeVisitor):
    def __init__(self):
        self.defined_names: Set[str] = set()

    @recursive
    def visit_FunctionDef(self, node: C.ASTFunctionT) -> None:
        self.defined_names.add(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    @recursive
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.defined_names.add(node.name)

    @recursive
    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)


class _ImportScanner(ast.NodeVisitor):
    ignore_modules_imports = ("__future__",)
    skip_import_comments_regex = "#.*(unimport: {0,1}skip|noqa)"

    def __init__(
        self,
        *,
        source: str,
        names: List[Name] = [],
        include_star_import: bool = False,
    ):
        self.source = source
        self.names = names
        self.include_star_import = include_star_import

        self.imports: List[C.ImportT] = []
        self.any_import_error = False
        self.defined_names: Set[str] = set()

    def traverse(self, tree) -> None:
        defined_name_scanner = _DefinedNameScanner()
        defined_name_scanner.visit(tree)
        self.defined_names = defined_name_scanner.defined_names
        self.visit(tree)

    @recursive
    def visit_Import(self, node: ast.Import) -> None:
        if self.skip_import(node):
            return
        for column, alias in enumerate(node.names):
            name = alias.asname or alias.name
            self.imports.append(
                Import(
                    lineno=node.lineno,
                    column=column + 1,
                    name=name,
                    package=alias.name,
                )
            )

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if self.skip_import(node):
            return
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
            name = package if is_star else alias_name
            suggestions = self.get_suggestions(package) if is_star else []
            self.imports.append(
                ImportFrom(
                    lineno=node.lineno,
                    column=column + 1,
                    name=name,
                    star=is_star,
                    suggestions=suggestions,
                    package=package,
                )
            )

    def visit_Try(self, node: ast.Try) -> None:
        def any_import_error(items) -> bool:
            for item in items:
                if (
                    isinstance(item, ast.Name)
                    and item.id in {"ModuleNotFoundError", "ImportError"}
                ) or (
                    isinstance(item, ast.Tuple) and any_import_error(item.elts)
                ):
                    return True
            else:
                return False

        self.any_import_error = any_import_error(
            handle.type for handle in node.handlers
        )
        self.generic_visit(node)
        self.any_import_error = False

    def skip_import(self, node: Union[ast.Import, ast.ImportFrom]) -> bool:
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
        names = {name.name.split(".")[0] for name in self.names}
        from_names = _ImportableScanner().get_names(package)
        return sorted(from_names & (names - self.defined_names))


class _NameScanner(ast.NodeVisitor):
    def __init__(self):
        self.names: List[Name] = []

    @recursive
    def visit_FunctionDef(self, node: C.ASTFunctionT) -> None:
        self._type_comment(node)

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

    @recursive
    def visit_Name(self, node: ast.Name) -> None:
        if not isinstance(node.parent, ast.Attribute):  # type: ignore
            self.names.append(Name(lineno=node.lineno, name=node.id))

    @recursive
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if not isinstance(node.value, ast.Call):
            names = []
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Attribute):
                    names.append(sub_node.attr)
                elif isinstance(sub_node, ast.Name):
                    names.append(sub_node.id)
            names.reverse()
            self.names.append(Name(lineno=node.lineno, name=".".join(names)))

    @recursive
    def visit_Assign(self, node: ast.Assign) -> None:
        self._type_comment(node)

    @recursive
    def visit_arg(self, node: ast.arg) -> None:
        self._type_comment(node)

    @recursive
    def visit_Subscript(self, node: ast.Subscript) -> None:
        # type_variable
        # type_var = List["object"] etc.

        def visit_constant_str(node: Union[ast.Constant, ast.Str]) -> None:
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

    @recursive
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

    def traverse(self, tree) -> None:
        self.visit(tree)
        """
        Receive items on the __all__ list
        """
        importable_visitor = _ImportableScanner()
        importable_visitor.traverse(tree)
        for node in importable_visitor.importable_nodes:
            if isinstance(node, ast.Constant):
                self.names.append(
                    Name(lineno=node.lineno, name=str(node.value), is_all=True)
                )
            elif isinstance(node, ast.Str):
                self.names.append(
                    Name(lineno=node.lineno, name=node.s, is_all=True)
                )

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


class _ImportableScanner(ast.NodeVisitor):
    def __init__(self) -> None:
        self.importable_nodes: List[
            Union[ast.Str, ast.Constant]
        ] = []  # nodes on the __all__ list
        self.suggestions_nodes: List[C.ASTImportableT] = []  # nodes on the CFN

    def traverse(self, tree) -> None:
        relate(tree)
        self.visit(tree)

    @recursive
    def visit_CFN(self, node: C.CFNT) -> None:
        if not first_occurrence(node, C.DefTuple):
            self.suggestions_nodes.append(node)

    visit_ClassDef = visit_CFN
    visit_FunctionDef = visit_CFN
    visit_AsyncFunctionDef = visit_CFN

    @recursive
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.suggestions_nodes.append(alias)

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if not node.names[0].name == "*":
            for alias in node.names:
                self.suggestions_nodes.append(alias)

    @recursive
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

    @recursive
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

    def get_names(self, package: str) -> FrozenSet[str]:
        if utils.is_std(package):
            return utils.get_dir(package)
        source = utils.get_source(package)
        if source:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                return frozenset()
            else:
                visitor = self.__class__()
                visitor.traverse(tree)
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


class Scanner(ast.NodeVisitor):
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

        self.names: List[Name] = []
        self.imports: List[C.ImportT] = []
        self.import_names: List[str] = []

    def traverse(self) -> None:
        if not self.skip_file():
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
            else:
                relate(tree)
                name_scanner = _NameScanner()
                name_scanner.traverse(tree)
                self.names.extend(name_scanner.names)
                import_scanner = _ImportScanner(
                    source=self.source,
                    names=self.names,
                    include_star_import=self.include_star_import,
                )
                import_scanner.traverse(tree)
                self.imports.extend(import_scanner.imports)
                self.import_names.extend([imp.name for imp in self.imports])

    def get_unused_imports(self) -> Iterator[C.ImportT]:
        for imp in self.imports:
            # duplicate import
            if self.is_duplicate(
                imp.name
            ) and not self.is_duplicate_import_used(imp):
                yield imp
            # star import
            elif (
                self.include_star_import
                and isinstance(imp, ImportFrom)
                and imp.star
            ):
                yield imp
            # normal import
            elif not self.is_import_used(imp):
                yield imp

    def is_duplicate_import_used(self, imp: C.ImportT) -> bool:
        for name in self.names:
            if name.match(imp) and imp == self.get_nearest_duplicate_imports(
                imp.name, name.lineno
            ):
                return True
        return False

    def is_import_used(self, imp: C.ImportT) -> bool:
        return any(name.match(imp) for name in self.names)

    @functools.lru_cache(maxsize=None)
    def get_nearest_duplicate_imports(
        self, import_name: str, name_lineno: int
    ) -> C.ImportT:
        return [
            imp
            for imp in self.imports
            if import_name == imp.name
            if self.is_duplicate(imp.name)
            if imp.lineno < name_lineno
        ][-1]

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.import_names.clear()

    def is_duplicate(self, name: str) -> bool:
        return self.import_names.count(name) > 1

    def skip_file(self) -> bool:
        return bool(
            re.search(self.skip_file_regex, self.source, re.IGNORECASE)
        )
