import ast
import importlib
import inspect
import sys


def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    "To detect unused import using ast"
    ignore_imports = ["__future__"]

    def __init__(self, source=None):
        self.names = list()
        self.imports = list()
        self.classes = list()
        self.method_names = list()
        self.functions = list()
        if source:
            self.run_visit(source)

    @recursive
    def visit_ClassDef(self, node):
        for function_node in [body for body in node.body]:
            if isinstance(function_node, ast.FunctionDef):
                self.method_names.append(function_node.name)
        self.classes.append(
            dict(lineno=node.lineno, name=node.name, node_name="class")
        )

    @recursive
    def visit_FunctionDef(self, node):
        if node.name not in self.method_names:
            self.functions.append(
                dict(lineno=node.lineno, name=node.name, node_name="function")
            )

    @recursive
    def visit_Import(self, node):
        star = False
        module_name = None
        if hasattr(node, "module"):
            module_name = node.module
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            if name == "*":
                star = True
            if (module_name or name) not in self.ignore_imports:
                try:
                    module = importlib.import_module(module_name or name)
                except ModuleNotFoundError:
                    module = None
                    if star:
                        continue
                self.imports.append(
                    dict(
                        lineno=node.lineno,
                        name=name,
                        node_name="import",
                        star=star,
                        module=module,
                    )
                )

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore_imports[1:]:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        self.names.append(
            dict(lineno=node.lineno, name=node.id, node_name="name")
        )

    @recursive
    def visit_Attribute(self, node):
        local_attr = list()
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
            dict(
                lineno=node.lineno, name=".".join(local_attr), node_name="name"
            )
        )

    def get_unused_imports(self):
        # TODO removed to session
        for imp in self.imports:
            if not imp["star"]:
                len_dot = len(imp["name"].split("."))
                for name in self.names:
                    if (
                        ".".join(name["name"].split(".")[:len_dot])
                        == imp["name"]
                    ):
                        break
                else:
                    yield imp

    def from_import_star(self):
        # TODO removed to session
        for imp in self.imports:
            if imp["star"]:
                if imp["module"].__name__ not in sys.builtin_module_names:
                    to_ = {to_cfv["name"] for to_cfv in self.names}
                    s = self.__class__(source=inspect.getsource(imp["module"]))
                    modules = [
                        from_cfv
                        for from_cfv in {
                            from_cfv["name"]
                            for from_cfv in s.names + s.classes + s.functions
                        }
                        if from_cfv in to_
                    ]
                    yield dict(imp=imp, modules=modules)

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.method_names.clear()
        self.functions.clear()
