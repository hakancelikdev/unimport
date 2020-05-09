import ast
import importlib
import inspect
import sys


def recursive(func):
    """decorator to make visitor work recursive"""

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    """To detect unused import using ast"""

    ignore_imports = ["__future__", "__doc__"]
    ignore_names = ["print"]

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
                except (ModuleNotFoundError, ValueError):
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
        if node.id not in self.ignore_names:
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
        self.names.append(
            {"lineno": node.lineno, "name": ".".join(local_attr)}
        )

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()

    def imp_star_True(self, imp):
        if imp["module"]:
            if imp["module"].__name__ not in sys.builtin_module_names:
                to_ = {to_cfv["name"] for to_cfv in self.names}
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
        for name in self.names:
            if name["name"].startswith(imp["name"]):
                break
        else:
            return imp

    def get_unused_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp["name"]):
                for name in self.names:
                    if name["name"].startswith(imp["name"]) and not self.is_duplicate_used(name, imp):
                        # This import: used
                        break
                else:
                    # This import: unused
                    yield imp
            else:
                res = getattr(self, f"imp_star_{imp['star']}")(imp)
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
                if (
                    dup_imp["lineno"] < name["lineno"]
                    and dup_imp["name"] == name["name"]
                ):
                    nearest = dup_imp
            return nearest

        return imp != find_nearest_imp(name)
