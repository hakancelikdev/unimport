import ast


def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class DetectUnusedImport(ast.NodeVisitor):
    "To detect unused import using ast"
    ignore = ["*", "__future__"]

    def __init__(self, source):
        self.names = list()
        self.imports = list()
        self.import_names = set()
        self.visit(ast.parse(source=source))

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
        self.names.append(".".join(local_attr))
