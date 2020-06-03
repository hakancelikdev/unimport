import ast
import builtins
import contextlib
import importlib
import inspect
import io
import sys
import tokenize

PY38_PLUS = sys.version_info >= (3, 8)


def recursive(func):
    """decorator to make visitor work recursive"""

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    """To detect unused import using ast"""

    ignore_imports = ["__future__"]
    skip_comments = ["#unimport:skip", "# unimport:skip"]

    def __init__(self, source=None, include_star_import=False):
        self.include_star_import = include_star_import
        self.names = []
        self.imports = []
        self.classes = []
        self.functions = []
        if source:
            self.run_visit(source)

    @recursive
    def visit_ClassDef(self, node):
        for function_node in [body for body in node.body]:
            if isinstance(function_node, ast.FunctionDef):
                function_node.class_def = True
        self.classes.append({"lineno": node.lineno, "name": node.name})

    @recursive
    def visit_FunctionDef(self, node):
        if not hasattr(node, "class_def"):
            self.functions.append({"lineno": node.lineno, "name": node.name})

    @recursive
    def visit_Import(self, node):
        if self.skip_import(node.lineno):
            return
        star = False
        module_name = None
        module = None
        if hasattr(node, "module"):
            module_name = node.module
        for alias in node.names:
            if alias.asname:
                name = alias.asname
            else:
                name = alias.name
            package = module_name or alias.name
            if package not in self.ignore_imports:
                if name == "*":
                    star = True
                    name = package
                try:
                    module = importlib.import_module(package)
                except ImportError:
                    pass
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
        self.visit_Import(node)

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
                with contextlib.suppress(SyntaxError):
                    comment_string = token.string.split("# type: ")
                    if comment_string != [token.string]:
                        functype = ast.parse(
                            comment_string[1], mode="func_type"
                        )
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
        if hasattr(node, "attr"):
            local_attr.append(node.attr)
        while True:
            if hasattr(node, "value"):
                if isinstance(node.value, ast.Attribute):
                    node = node.value
                    if hasattr(node, "attr"):
                        local_attr.append(node.attr)
                elif isinstance(node.value, ast.Call):
                    node = node.value
                    if isinstance(node.func, ast.Name):
                        local_attr.append(node.func.id)
                elif isinstance(node.value, ast.Name):
                    node = node.value
                    local_attr.append(node.id)
                else:
                    break
            else:
                break
        local_attr.reverse()
        self.names.append(
            {"lineno": node.lineno, "name": ".".join(local_attr)}
        )

    @recursive
    def visit_Assign(self, node):
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(
            node.value, (ast.List, ast.Tuple)
        ):
            for item in node.value.elts:
                get_name = None
                if (
                    PY38_PLUS
                    and isinstance(item, ast.Constant)
                    and isinstance(item.value, ast.Str)
                ):
                    get_name = item.value
                elif isinstance(item, ast.Str):
                    get_name = item.s
                if get_name:
                    self.names.append(
                        {"lineno": node.lineno, "name": get_name}
                    )

    def run_visit(self, source):
        self.source = source
        if PY38_PLUS:
            for node in self.iter_type_comments():
                self.names.append({"lineno": node.lineno, "name": node.id})
        with contextlib.suppress(SyntaxError):
            self.visit(ast.parse(self.source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()

    def skip_import(self, lineno):
        line = self.source.split("\n")[lineno - 1]
        start_comment = line.find("#")
        for skip_comment in self.skip_comments:
            if (
                skip_comment
                == line[
                    start_comment : start_comment + len(skip_comment)
                ].lower()
            ):
                return True

    def get_names(self):
        imp_match_built_in = [
            imp["name"]
            for imp in self.imports
            if hasattr(builtins, imp["name"])
        ]
        for name in self.names:
            if any(
                [imp_name == name["name"] for imp_name in imp_match_built_in]
            ) or not hasattr(builtins, name["name"]):
                yield name

    def imp_star_True(self, imp):
        if imp["module"]:
            if imp["module"].__name__ not in sys.builtin_module_names:
                to_ = {to_cfv["name"] for to_cfv in self.get_names()}
                try:
                    s = self.__class__(inspect.getsource(imp["module"]))
                except OSError:
                    pass
                else:
                    all_object = s.classes + s.functions + s.names
                    all_name = {from_cfv["name"] for from_cfv in all_object}
                    imp["modules"] = sorted(
                        {cfv for cfv in all_name if cfv in to_}
                    )
        return imp

    def imp_star_False(self, imp):
        for name in self.get_names():
            if name["name"].startswith(imp["name"]):
                # used
                break
        else:
            # unused
            return imp

    def get_unused_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp["name"]):
                for name in self.get_names():
                    if name["name"].startswith(
                        imp["name"]
                    ) and not self.is_duplicate_used(name, imp):
                        # This import: used
                        break
                else:
                    # This import: unused
                    yield imp
            else:
                res = False
                is_star_import = imp["star"]
                if is_star_import:
                    if self.include_star_import:
                        res = getattr(self, f"imp_star_{is_star_import}")(imp)
                else:
                    res = self.imp_star_False(imp)
                if res:
                    yield res

    def is_duplicate(self, name):
        return [imp["name"] for imp in self.imports].count(name) > 1

    def get_duplicate_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp["name"]):
                yield imp

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
