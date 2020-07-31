"""
This module performs static analysis using AST on the python code that's given as a string and reports its findings.
"""

import ast
import builtins
import contextlib
import functools
import importlib
import inspect
import io
import re
import sys
import tokenize
from types import ModuleType
from typing import (
    Any,
    Callable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    TypeVar,
    Union,
    cast,
)

from unimport.color import Color

PY38_PLUS = sys.version_info >= (3, 8)
BUILTINS = {_build for _build in dir(builtins) if not _build.startswith("_")}

Function = TypeVar("Function", bound=Callable[..., Any])


class Name(NamedTuple):
    lineno: int
    name: str


class Import(NamedTuple):
    lineno: int
    name: str
    star: bool
    module: Optional[ModuleType]
    modules: List[str]


def recursive(func: Function) -> Function:
    """decorator to make visitor work recursive"""

    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):
        func(self, node, *args, **kwargs)
        self.generic_visit(node)

    return cast(Function, wrapper)


class Scanner(ast.NodeVisitor):
    ignore_imports = ["__future__"]
    ignore_import_names = ["__all__", "__doc__"]
    skip_file_regex = "#\s*(unimport:\s{0,1}skip_file)"
    skip_comments_regex = "#\s*(unimport:\s{0,1}skip|noqa)"

    def __init__(
        self, *, include_star_import: bool = False, show_error: bool = False,
    ):
        """
        If include_star_import is True during the analysis, it takes into account start imports, if it's False, it doesn't.

        E.g.: from x import * is a star import.

        If show_error is True during the analysis, errors are displayed.
        """
        self.include_star_import = include_star_import
        self.show_error = show_error
        self.imports: List[Import] = []
        self.classes: List[Name] = []
        self.functions: List[Name] = []
        self.names: List[Name] = []
        self.import_names: List[str] = []
        self.unused_imports: List[Import] = []
        self.any_import_error = False

    @recursive
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        When include_star_import becomes True, instead of suggesting star,
        it analyses class names and suggests one of the analyzed class's name.

        E.g.: from os import *
        print(PathLike)

        At this point from os import * becomes > from os import PathLike
        """
        self.classes.append(Name(lineno=node.lineno, name=node.name))

    @recursive
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        When include_star_import becomes True, instead of suggesting star,
        it analyses function names and suggests one of the analyzed function's name.

        E.g.: from os import *
        print(walk)

        At this point from os import * becomes > from os import walk
        """
        if not Relate.first_occurrence(node, ast.ClassDef):
            self.functions.append(Name(lineno=node.lineno, name=node.name))

    def alike_import(
        self,
        node: Union[ast.Import, ast.ImportFrom],
        module_name: Optional[str] = None,
        star: bool = False,
    ) -> None:
        if self.skip_import(node):
            return
        module = None
        for alias in node.names:
            package = module_name or alias.name
            alias_name = alias.asname or alias.name
            name = package if star else alias_name
            if package in self.ignore_imports or (
                star and not self.include_star_import
            ):
                return
            with contextlib.suppress(BaseException):
                module = importlib.import_module(package)
            self.imports.append(
                Import(
                    lineno=node.lineno,
                    name=name,
                    star=star,
                    module=module,
                    modules=[],
                )
            )

    def visit_Str(self, node: ast.Str) -> None:
        constant = ast.Constant(node.s)
        try:
            constant.parent = node.parent  # type: ignore
        except AttributeError:
            with contextlib.suppress(SyntaxError):
                self.visit(ast.parse(node.s, mode="eval"))
        else:
            self.visit_Constant(constant, id_=id(node))

    @recursive
    def visit_Constant(
        self, node: ast.Constant, id_: Optional[int] = None
    ) -> None:
        id_ = id_ or id(node)
        if not isinstance(node.value, (str, bytes)):
            return
        try:
            parent = Relate.first_occurrence(node, ast.FunctionDef)
        except AttributeError:
            with contextlib.suppress(SyntaxError):
                self.visit(ast.parse(node.value, mode="eval"))
        else:
            is_annasign_and_arg = any(
                type_parent in {ast.AnnAssign, ast.arg}
                for type_parent in map(type, Relate.get_parents(node))
            )
            if (parent and id(parent.returns) == id_) or is_annasign_and_arg:
                with contextlib.suppress(SyntaxError):
                    self.visit(ast.parse(node.value, mode="eval"))

    @recursive
    def visit_Import(self, node: ast.Import) -> None:
        self.alike_import(node)

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.alike_import(
            node, module_name=node.module, star=node.names[0].name == "*"
        )

    @recursive
    def visit_Name(self, node: ast.Name) -> None:
        self.names.append(Name(lineno=node.lineno, name=node.id))

    def iter_type_comments(self):
        """
        This feature is only available for python 3.8.

        PEP 526 -- Syntax for Variable Annotations
        https://www.python.org/dev/peps/pep-0526/

        https://docs.python.org/3.8/library/ast.html#ast.parse

        """
        buffer = io.StringIO(self.source)
        for token in tokenize.generate_tokens(buffer.readline):
            if token.type == tokenize.COMMENT:
                comment_string = token.string.split("# type: ")
                if comment_string != [token.string]:
                    try:
                        functype = ast.parse(
                            comment_string[1], mode="func_type"
                        )
                    except SyntaxError as err:
                        if self.show_error:
                            error_messages = f"{token.line}\n{comment_string[1]} {Color(str(err)).red}"
                            print(error_messages)
                    else:
                        for node in ast.walk(
                            ast.Module(functype.argtypes + [functype.returns])
                        ):
                            if isinstance(node, ast.Name) and isinstance(
                                node.ctx, ast.Load
                            ):
                                self.visit(node)

    @recursive
    def visit_Attribute(self, node: ast.Attribute) -> None:
        local_attr = []
        for attr_node in ast.walk(node):
            if isinstance(attr_node, ast.Name):
                local_attr.append(attr_node.id)
            elif isinstance(attr_node, ast.Attribute):
                local_attr.append(attr_node.attr)
        local_attr.reverse()
        self.names.append(Name(lineno=node.lineno, name=".".join(local_attr)))

    @recursive
    def visit_Assign(self, node: ast.Assign) -> None:
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(
            node.value, (ast.List, ast.Tuple, ast.Set)
        ):
            for item in node.value.elts:
                if isinstance(item, ast.Str):
                    self.names.append(Name(lineno=node.lineno, name=item.s))

    def visit_Try(self, node: ast.Try) -> None:
        def any_import_error(items):
            for item in items:
                if isinstance(item, ast.Name) and item.id in {
                    "ModuleNotFoundError",
                    "ImportError",
                }:
                    return True
                elif isinstance(item, ast.Tuple) and any_import_error(
                    item.elts
                ):
                    return True
            else:
                return False

        self.any_import_error = any_import_error(
            handle.type for handle in node.handlers
        )
        self.generic_visit(node)
        self.any_import_error = False

    def scan(self, source: str) -> None:
        self.source = source
        if self.skip_file():
            return
        if PY38_PLUS:
            self.iter_type_comments()
        with contextlib.suppress(SyntaxError):
            tree = ast.parse(self.source)
            Relate(tree)
            self.visit(tree)
        self.import_names = [imp.name for imp in self.imports]
        self.names = list(self.get_names())
        self.unused_imports = list(self.get_unused_imports())

    def clear(self) -> None:
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()
        self.import_names.clear()
        self.unused_imports.clear()

    def skip_import(self, node: Union[ast.ImportFrom, ast.Import]) -> bool:
        return (
            bool(
                re.search(
                    self.skip_comments_regex,
                    self.source.splitlines()[node.lineno - 1],
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
        imp_match_built_in = BUILTINS & set(self.import_names)
        yield from filter(
            lambda name: list(
                filter(
                    lambda imp_name: imp_name == name.name, imp_match_built_in,
                )
            )
            or not hasattr(builtins, name.name),
            self.names,
        )

    def get_suggestion_modules(self, imp: Import) -> List[str]:
        if imp.module is not None:
            with contextlib.suppress(OSError, TypeError):
                scanner = self.__class__()
                scanner.scan(inspect.getsource(imp.module))
                objects = scanner.classes + scanner.functions + scanner.names
                from_all_name = {obj.name for obj in objects}
                to_names = {
                    to_cfv.name
                    for to_cfv in self.names
                    if to_cfv.name not in self.ignore_import_names
                }
                suggestion_modules = sorted(from_all_name & to_names)
                return suggestion_modules
        return []

    def get_unused_imports(self) -> Iterator[Import]:
        for imp in self.imports:
            if self.is_duplicate(imp.name) and not self.is_duplicate_used(imp):
                yield imp
            else:
                if imp.star and self.include_star_import:
                    imp.modules.extend(self.get_suggestion_modules(imp))
                    yield imp
                else:
                    if not list(
                        filter(lambda name: name.name == imp.name, self.names,)
                    ):
                        yield imp

    def is_duplicate(self, name: str) -> bool:
        return self.import_names.count(name) > 1

    def get_duplicate_imports(self) -> Iterator[Import]:
        yield from filter(
            lambda imp: self.is_duplicate(imp.name), self.imports
        )

    def is_duplicate_used(self, imp: Import) -> bool:
        def find_nearest_imp(name: Name) -> Import:
            nearest = imp
            for duplicate in self.get_duplicate_imports():
                if (
                    duplicate.lineno < name.lineno
                    and name.name == duplicate.name
                ):
                    nearest = duplicate
            return nearest

        for name in self.names:
            if name.name == imp.name and imp == find_nearest_imp(name):
                return True
        return False


class Relate:
    # https://tree.science/using-ancestral-chains-in-ast.html

    def __init__(self, tree: ast.Module) -> None:
        tree.parent = None  # type: ignore
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child.parent = parent  # type: ignore

    @classmethod
    def get_parents(cls, node: ast.AST) -> Iterator[ast.AST]:
        parent = node
        while parent:
            parent = parent.parent  # type: ignore
            if parent is None:
                continue
            yield parent

    @classmethod
    def first_occurrence(cls, node: ast.AST, *ancestors):
        for parent in cls.get_parents(node):
            if type(parent) in ancestors:
                return parent
        else:
            return False
