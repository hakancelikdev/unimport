import ast
import os
import sys
import tokenize


def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class UnImport(ast.NodeVisitor):
    def __init__(self, source):
        self.names = list()
        self.imports = list()
        self.visit(ast.parse(source=source))

    @recursive
    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            if name == "*":
                continue
            self.imports.append(dict(lineno=node.lineno, name=name))

    @recursive
    def visit_ImportFrom(self, node):
        self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        if not isinstance(node.ctx, ast.Store):
            self.names.append(dict(lineno=node.lineno, name=node.id))

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
        self.names.append(dict(lineno=node.lineno, name=".".join(local_attr)))
        self.generic_visit(node)

    def get_diff(self):
        name_names = set([name["name"] for name in self.names])
        for imp in self.imports:
            len_dot = len(imp["name"].split("."))
            for name in name_names:
                if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                    break
            else:
                yield imp


def unimport():
    try:
        _unimport_conf = tokenize.open(
            f"{os.getcwd()}//{sys.argv[1]}//.unimport.cfg"
        ).readlines()
    except FileNotFoundError:
        _unimport_conf = None
    else:
        _unimport_conf = [conf.replace("\n", "") for conf in _unimport_conf]
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            file = os.path.join(root, name)
            if file.endswith(".py"):
                if _unimport_conf:
                    diff = set(file.split(os.sep)) - set(_unimport_conf)
                    if diff != set(file.split(os.sep)):
                        continue
                unimport = UnImport(source=open(file, "r", encoding="utf-8").read())
                for unused in unimport.get_diff():
                    unused.update(path=file)
                    print(unused)


if __name__ == "__main__":
    # test
    import inspect
    import os

    unused_import = UnImport(source=inspect.getsource(os))
    for unused in unused_import.get_diff():
        print(unused)
