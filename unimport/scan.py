import ast


def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    "To detect unused import using ast"
    ignore_imports = ["*", "__future__"]

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
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            if name in self.ignore_imports:
                continue
            self.imports.append(dict(lineno=node.lineno, name=name, node_name="import"))
            self.import_names.add(name)

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore_imports[1:]:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        # if isinstance(node.ctx, ast.Store):
        #     if node.id in self.import_names:
        #         self.names.append(dict(lineno=node.lineno, name=node.id, node_name="name"))
        # else:
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

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.import_names.clear()
        self.classes.clear()
        self.method_names.clear()
        self.functions.clear()
