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
                except (ModuleNotFoundError, ValueError):
                    module = None
                    if star:
                        continue
                self.imports.append(
                    {
                        "lineno": node.lineno,
                        "name": name,
                        "star": star,
                        "module": module,
                    }
                )

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore_imports:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        self.names.append({"lineno": node.lineno, "name": node.id})

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
        self.names.append({"lineno": node.lineno, "name": ".".join(local_attr)})

    def _imp_is_star(self, imp):
        if imp["module"].__name__ not in sys.builtin_module_names:
            to_ = {to_cfv["name"] for to_cfv in self.names}
            try:
                s = self.__class__(inspect.getsource(imp["module"]))
            except OSError:
                return {"imp": imp, "modules": []}
            imp["modules"] = sorted(
                {
                    cfv
                    for cfv in {
                        from_cfv["name"]
                        for from_cfv in s.names + s.classes + s.functions
                    }
                    if cfv in to_
                }
            )
            return imp

    def _imp_is_not_star(self, imp):
        for name in self.names:
            if (
                ".".join(
                    name["name"].split(".")[: len(imp["name"].split("."))]
                )
                == imp["name"]
            ):
                break
        else:
            return imp

    def get_unused_imports(self):
        for imp in self.imports:
            if imp["star"]:
                yield self._imp_is_star(imp)
            else:
                res = self._imp_is_not_star(imp)
                if res:
                    yield res

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()
