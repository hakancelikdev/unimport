import ast


def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    "To detect unused import using ast"
    ignore = ["*", "__future__"]

    def __init__(self, source=None):
        self.names = list()
        self.imports = list()
        self.import_names = set()
        if source:
            self.visit(ast.parse(source))

    def iter_imports(self, source):
        self.visit(ast.parse(source))
        for imp in self.imports:
            len_dot = len(imp["name"].split("."))
            for name in self.names:
                if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                    break
            else:
                yield imp

        self.clear()

    def clear(self):
        self.names.clear()
        self.imports.clear()
        self.import_names.clear()

    @recursive
    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            if name in self.ignore:
                continue
            self.imports.append(dict(lineno=node.lineno, name=name))
            self.import_names.add(name)

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore[1:]:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if node.id in self.import_names:
                self.names.append(node.id)
        else:
            self.names.append(node.id)

    def visit_Attribute(self, node):
        local_attr = list()
        for node in ast.walk(node):
            if isinstance(node, ast.Name):
                local_attr.append(node.id)
            elif isinstance(node, ast.Attribute):
                local_attr.append(node.attr)
        local_attr.reverse()
        self.names.append(".".join(local_attr))
