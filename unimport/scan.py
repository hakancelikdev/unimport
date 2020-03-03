import ast
import sys
import importlib
import inspect

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
        self.import_names = set()
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
        self.classes.append(dict(lineno=node.lineno, name=node.name, node_name="class"))

    @recursive
    def visit_FunctionDef(self, node):
        if node.name not in self.method_names:
            self.functions.append(dict(lineno=node.lineno, name=node.name, node_name="function"))

    @recursive
    def visit_Import(self, node):
        if hasattr(node, "module"):
            star = True
            name = node.module
        else:
            star = False
            for alias in node.names:
                if alias.asname is not None:
                    name = alias.asname
                else:
                    name = alias.name
        if name not in self.ignore_imports:
            try:
                module = importlib.import_module(name)
            except ModuleNotFoundError:
                module = None
            self.imports.append(dict(lineno=node.lineno, name=name, node_name="import", star=star, module=module))
            self.import_names.add(name)

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore_imports[1:]:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        self.names.append(dict(lineno=node.lineno, name=node.id, node_name="name"))

    def visit_Attribute(self, node):
        lineno = node.lineno
        local_attr = list()
        for node in ast.walk(node):
            if isinstance(node, ast.Name):
                local_attr.append(node.id)
            elif isinstance(node, ast.Attribute):
                local_attr.append(node.attr)
        local_attr.reverse()
        self.names.append(dict(lineno=lineno, name=".".join(local_attr), node_name="name"))

    def get_unused_imports(self):
        # TODO removed to session
        for imp in self.imports:
            len_dot = len(imp["name"].split("."))
            for name in self.names:
                if ".".join(name["name"].split(".")[:len_dot]) == imp["name"]:
                    break
            else:
                yield imp
        # self.scanner.clear()

    def from_import_star(self):
        # TODO removed to session
        for imp in self.imports:
            if imp["star"]:
                if imp["module"].__name__ not in sys.builtin_module_names:
                    to_ = {to_cfv["name"] for to_cfv in self.names}
                    s = self.__class__(source=inspect.getsource(imp["module"]))
                    yield "from " + imp["module"].__name__ + " import " , *[from_cfv for from_cfv in {from_cfv["name"] for from_cfv in s.names + s.classes + s.functions} if from_cfv in to_]

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.import_names.clear()
        self.classes.clear()
        self.method_names.clear()
        self.functions.clear()
