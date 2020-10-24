"""This module performs static analysis using AST on the python code that's
given as a string and reports its findings."""
import ast
import contextlib
import functools
import re
from typing import Dict, FrozenSet, Iterator, List, Optional, Union, cast

from unimport import color
from unimport import constants as C
from unimport.relate import first_occurrence, get_parents, relate
from unimport.statement import Import, ImportFrom, Name
from unimport.utils import get_dir, get_source, is_std, recover_comments


def recursive(func: C.Function) -> C.Function:
    """decorator to make visitor work recursive."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.generic_visit(*args)

    return cast(C.Function, wrapper)


class Scanner(ast.NodeVisitor):
    ignore_modules_imports = ("__future__",)
    ignore_alias_imports = ("__all__", "__doc__")
    skip_file_regex = "#.*(unimport: {0,1}skip_file)"
    skip_comments_regex = "#.*(unimport: {0,1}skip|noqa)"

    def __init__(
        self,
        *,
        include_star_import: bool = False,
        show_error: bool = False,
    ):
        """If include_star_import is True during the analysis, it takes into
        account start imports, if it's False, it doesn't.

        E.g.: from x import * is a star import.
        If show_error is True during the analysis, errors are displayed.
        """
        self.include_star_import = include_star_import
        self.show_error = show_error
        self.imports: List[C.ImportT] = []
        self.names: List[Name] = []
        self.import_names: List[str] = []
        self.unused_imports: List[C.ImportT] = []
        self.any_import_error = False
        self._comments: Dict[int, str] = {}

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
    def visit_Import(self, node: ast.Import) -> None:
        if self.skip_import(node):
            return
        for column, alias in enumerate(node.names):
            name = alias.asname or alias.name
            if name in C.INITIAL_IMPORTS:
                name = name.split(".")[0]
            self.imports.append(
                Import(
                    lineno=node.lineno,
                    column=column + 1,
                    name=name,
                    package=alias.name,
                )
            )
            self.import_names.append(name)

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if self.skip_import(node):
            return
        is_star = node.names[0].name == "*"
        for column, alias in enumerate(node.names):
            if not node.level:
                package = node.module
            else:
                package = "." * node.level
            alias_name = alias.asname or alias.name
            if (
                (package in self.ignore_modules_imports)
                or (alias_name in self.ignore_alias_imports)
                or (is_star and not self.include_star_import)
            ):
                return
            name = package if is_star else alias_name
            self.imports.append(
                ImportFrom(
                    lineno=node.lineno,
                    column=column + 1,
                    name=name,
                    star=is_star,
                    suggestions=[],
                    package=package,
                )
            )
            self.import_names.append(name)

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
            name = ".".join(names)
            self.names.append(Name(lineno=node.lineno, name=name))

    @recursive
    def visit_Assign(self, node: ast.Assign) -> None:
        self._type_comment(node)

    @recursive
    def visit_arg(self, node: ast.arg) -> None:
        self._type_comment(node)

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
            if isinstance(node.slice.value, ast.Tuple):  # type: ignore
                for elt in node.slice.value.elts:  # type: ignore
                    if isinstance(elt, (ast.Constant, ast.Str)):
                        visit_constant_str(elt)
            else:
                if isinstance(node.slice.value, (ast.Constant, ast.Str)):  # type: ignore
                    visit_constant_str(node.slice.value)  # type: ignore

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

    def scan(self, source: str) -> None:
        self.source = source
        if self.skip_file():
            return
        if C.PY38_PLUS:
            self._comments = recover_comments(self.source)
        try:
            self.traverse(self.source)
        except SyntaxError:
            return None
        self.names = list(self.get_names())
        self.unused_imports = list(self.get_unused_imports())

    def _type_comment(self, node: ast.AST) -> None:
        if isinstance(node, C.ASTFunctionTuple):
            mode = "func_type"
        else:
            mode = "eval"
        type_comment = getattr(node, "type_comment", None)
        if type_comment is not None:
            self.join_visit(type_comment, node, mode=mode)

    def traverse(
        self,
        source: Union[str, bytes],
        mode: str = "exec",
        parent: Optional[ast.AST] = None,
    ) -> None:
        try:
            if C.PY38_PLUS:
                tree = ast.parse(source, mode=mode, type_comments=True)
            else:
                tree = ast.parse(source, mode=mode)
        except SyntaxError as err:
            if self.show_error:
                print(color.paint(str(err), color.RED))  # pragma: no cover
            raise err
        relate(tree, parent=parent)
        self.visit(tree)
        """
        Receive items on the __all__ list
        """
        importable_visitor = ImportableVisitor()
        importable_visitor.traverse(self.source)
        for node in importable_visitor.importable_nodes:
            if isinstance(node, ast.Constant):
                self.names.append(
                    Name(lineno=node.lineno, name=str(node.value))
                )
            elif isinstance(node, ast.Str):
                self.names.append(Name(lineno=node.lineno, name=node.s))

    def join_visit(
        self, value: str, node: ast.AST, *, mode: str = "eval"
    ) -> None:
        """A function that parses the value, copies locations from the node and
        includes them in self.visit."""
        if C.PY38_PLUS:
            tree = ast.parse(value, mode=mode, type_comments=True)
        else:
            tree = ast.parse(value, mode=mode)
        relate(tree, parent=node.parent)  # type: ignore
        for new_node in ast.walk(tree):
            ast.copy_location(new_node, node)
        self.visit(tree)

    def clear(self) -> None:
        self.names.clear()
        self.imports.clear()
        self.import_names.clear()
        self.unused_imports.clear()
        self._comments = {}

    def skip_import(self, node: Union[ast.Import, ast.ImportFrom]) -> bool:
        if C.PY38_PLUS:
            lines = ast.get_source_segment(self.source, node).splitlines()
            for lineno, comment in self._comments.items():
                with contextlib.suppress(IndexError):
                    lines[lineno - node.lineno] += " " + comment
            source_segment = "".join(lines)
        else:
            source_segment = self.source.splitlines()[node.lineno - 1]
        return (
            bool(
                re.search(
                    self.skip_comments_regex,
                    source_segment,
                    re.IGNORECASE,
                )
            )
            or self.any_import_error
        )

    def skip_file(self) -> bool:
        return bool(
            re.search(self.skip_file_regex, self.source, re.IGNORECASE)
        )

    def get_names(self) -> Iterator[Name]:
        imp_match_built_in = C.BUILTINS & set(self.import_names)
        for name in self.names:
            if [imp_name == name.name for imp_name in imp_match_built_in] or (
                name.name.split(".")[0] not in C.IGNORE_IMPORT_NAMES
                and name.name.split(".")[0] not in C.BUILTINS
            ):
                yield name

    def get_suggestions(self, package: str) -> List[str]:
        names = {to_cfv.name.split(".")[0] for to_cfv in self.names}
        from_names = ImportableVisitor().get_names(package)
        return sorted(from_names & names)

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
                imp.suggestions.extend(self.get_suggestions(imp.package))
                yield imp
            # normal import
            elif not self.is_import_used(imp):
                yield imp

    def is_duplicate(self, name: str) -> bool:
        return self.import_names.count(name) > 1

    @functools.lru_cache(maxsize=None)
    def get_duplicate_imports(self, import_name: str) -> List[C.ImportT]:
        return [
            imp
            for imp in self.imports
            if import_name == imp.name and self.is_duplicate(imp.name)
        ]

    def is_duplicate_import_used(self, imp: C.ImportT) -> bool:
        def find_nearest_imp(name: Name) -> C.ImportT:
            nearest = imp
            for duplicate in self.get_duplicate_imports(imp.name):
                if name.match(duplicate):
                    nearest = duplicate
            return nearest

        for name in self.names:
            if name.match(imp) and imp == find_nearest_imp(name):
                return True
        return False

    def is_import_used(self, imp: C.ImportT) -> bool:
        return any(name.match(imp) for name in self.names)


class ImportableVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.importable_nodes: List[
            Union[ast.Str, ast.Constant]
        ] = []  # nodes on the __all__ list
        self.suggestions_nodes: List[C.ASTImportableT] = []  # nodes on the CFN

    def traverse(self, source: str) -> None:
        tree = ast.parse(source)
        relate(tree)
        self.visit(tree)

    @recursive
    def visit_CFN(self, node: C.CFNT) -> None:
        if not first_occurrence(node, C.DefTuple):
            self.suggestions_nodes.append(node)

    visit_ClassDef = visit_CFN
    visit_FunctionDef = visit_CFN
    visit_AsyncFunctionDef = visit_CFN
    visit_Name = visit_CFN

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
        if is_std(package):
            return get_dir(package)
        visitor = self.__class__()
        source = get_source(package)
        if source:
            visitor.traverse(source)
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
