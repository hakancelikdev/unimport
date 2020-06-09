import ast
import builtins
import contextlib
import importlib
import inspect
import io
import re
import sys
import tokenize

from unimport.color import Color

PY38_PLUS = sys.version_info >= (3, 8)
SET_BUILTINS = set(dir(builtins))


def recursive(func):
    """decorator to make visitor work recursive"""

    def wrapper(self, node, *args, **kwargs):
        func(self, node, *args, **kwargs)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    """To detect unused import using ast"""

    ignore_imports = ["__future__"]
    ignore_import_names = ["__all__", "__doc__"]
    skip_comments_regex = "#\s*(unimport:skip|noqa)"
    any_import_error: bool = False

    def __init__(
        self, source=None, include_star_import=False, show_error=False
    ):
        self.include_star_import = include_star_import
        self.show_error = show_error
        self.names = []
        self.imports = []
        self.classes = []
        self.functions = []
        if source:
            self.run_visit(source)

    @recursive
    def visit_ClassDef(self, node):
        for function_node in ast.walk(node):
            if isinstance(function_node, ast.FunctionDef):
                function_node.class_def = True
        self.classes.append({"lineno": node.lineno, "name": node.name})

    @recursive
    def visit_FunctionDef(self, node):
        if not hasattr(node, "class_def"):
            self.functions.append({"lineno": node.lineno, "name": node.name})

    @recursive
    def visit_Import(self, node, module_name=None):
        if self.skip_import(node):
            return
        module = None
        for alias in node.names:
            package = module_name or alias.name
            alias_name = alias.asname or alias.name
            star = True if alias_name == "*" else False
            name = package if star else alias_name
            is_package_or_name_ignore = (
                package in self.ignore_imports
                or name in self.ignore_import_names
            )
            if is_package_or_name_ignore or (
                star and not self.include_star_import
            ):
                return
            with contextlib.suppress(ImportError, ValueError):
                module = importlib.import_module(package)
            self.imports.append(
                {
                    "lineno": node.lineno,
                    "name": name,
                    "star": star,
                    "module": module,
                    "modules": [],
                }
            )

    @recursive
    def visit_ImportFrom(self, node):
        self.visit_Import(node, node.module)

    @recursive
    def visit_Name(self, node):
        self.names.append({"lineno": node.lineno, "name": node.id})

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
                                yield node

    @recursive
    def visit_Attribute(self, node):
        local_attr = []
        for attr_node in ast.walk(node):
            if isinstance(attr_node, ast.Name):
                local_attr.append(attr_node.id)
            elif isinstance(attr_node, ast.Attribute):
                local_attr.append(attr_node.attr)
        local_attr.reverse()
        self.names.append(
            {"lineno": node.lineno, "name": ".".join(local_attr)}
        )

    @recursive
    def visit_Assign(self, node):
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(
            node.value, (ast.List, ast.Tuple, ast.Set)
        ):
            for item in node.value.elts:
                if isinstance(item, ast.Str):
                    self.names.append({"lineno": node.lineno, "name": item.s})

    def visit_Try(self, node):
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

    def run_visit(self, source):
        self.source = source
        if PY38_PLUS:
            for node in self.iter_type_comments():
                self.names.append({"lineno": node.lineno, "name": node.id})
        with contextlib.suppress(SyntaxError):
            self.visit(ast.parse(self.source))
        self.import_names = [imp["name"] for imp in self.imports]
        self.names = list(self.get_names())
        self.unused_imports = list(self.get_unused_imports())

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()

    def skip_import(self, node):
        return (
            re.search(
                self.skip_comments_regex,
                self.source.split("\n")[node.lineno - 1].lower(),
            )
            or self.any_import_error
        )

    def get_names(self):
        imp_match_built_in = SET_BUILTINS & set(self.import_names)
        yield from filter(
            lambda name: list(
                filter(
                    lambda imp_name: imp_name == name["name"],
                    imp_match_built_in,
                )
            )
            or not hasattr(builtins, name["name"]),
            self.names,
        )

    def get_suggestion_modules(self, imp):
        if imp["module"]:
            with contextlib.suppress(OSError, TypeError):
                scanner = self.__class__(inspect.getsource(imp["module"]))
                objects = scanner.classes + scanner.functions + scanner.names
                from_all_name = {obj["name"] for obj in objects}
                to_names = {to_cfv["name"] for to_cfv in self.names}
                suggestion_modules = sorted(from_all_name & to_names)
                return suggestion_modules
        return {}

    def get_unused_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp["name"]):
                if not list(
                    filter(
                        lambda name: name["name"].startswith(imp["name"])
                        and not self.is_duplicate_used(name, imp),
                        self.names,
                    )
                ):
                    yield imp
            else:
                if imp["star"] and self.include_star_import:
                    imp["modules"] = self.get_suggestion_modules(imp)
                    yield imp
                else:
                    if not list(
                        filter(
                            lambda name: name["name"].startswith(imp["name"]),
                            self.names,
                        )
                    ):
                        yield imp

    def is_duplicate(self, name):
        return self.import_names.count(name) > 1

    def get_duplicate_imports(self):
        yield from filter(
            lambda imp: self.is_duplicate(imp["name"]), self.imports
        )

    def is_duplicate_used(self, name, imp):
        def find_nearest_imp(name):
            nearest = ""
            for dup_imp in self.get_duplicate_imports():
                if dup_imp["lineno"] < name["lineno"] and name[
                    "name"
                ].startswith(dup_imp["name"]):
                    nearest = dup_imp
            return nearest

        return imp != find_nearest_imp(name)
