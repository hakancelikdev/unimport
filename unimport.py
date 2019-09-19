import ast
import os
import sys

def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper

class UnImport(ast.NodeVisitor):

    def __init__(self, source):
        self.names = list()
        self.attrs = list()
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
            local_attr.append(
                dict(lineno=node.lineno, name=node.__class__.__name__, attr=node.attr)
            )
        while True:
            if hasattr(node, "value"):
                if isinstance(node.value, ast.Attribute):
                    node = node.value
                    if hasattr(node, "attr"):
                        local_attr.append(
                            dict(
                                lineno=node.lineno,
                                name=node.__class__.__name__,
                                attr=node.attr,
                            )
                        )
                elif isinstance(node.value, ast.Call):
                    node = node.value
                    if isinstance(node.func, ast.Name):
                        local_attr.append(
                            dict(
                                lineno=node.lineno,
                                name=node.__class__.__name__,
                                attr=node.func.id,
                            )
                        )
                elif isinstance(node.value, ast.Name):
                    node = node.value
                    local_attr.append(
                        dict(
                            lineno=node.lineno,
                            name=node.__class__.__name__,
                            attr=node.id,
                        )
                    )
                else:
                    break

            else:
                break
        local_attr.reverse()
        self.attrs.append(local_attr)
        self.generic_visit(node)


def unimport():
    try:
        _unimport_conf = open(f"{os.getcwd()}//{sys.argv[1]}//.unimport.cfg","r").readlines()
    except FileNotFoundError:
        _unimport_conf = None
    else:
        _unimport_conf = [conf.replace("\n", "") for conf in _unimport_conf]
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            file = os.path.join(root, name)
            if file.endswith(".py"):
                if _unimport_conf:
                    diff = (set(file.split("\\")) - set(_unimport_conf))
                    if diff != set(file.split("\\")):
                        continue
                unimport = UnImport(source=open(file, "r", encoding="utf-8").read())
                names = unimport.names
                imports = unimport.imports
                attrs = unimport.attrs
                for attr in attrs:
                    names.append(
                        dict(
                            lineno=attr[0]["lineno"],
                            name=".".join([atr["attr"] for atr in attr]),
                        )
                    )
                name_names = set(
                    [name["name"].split(".")[0] for name in names]
                )
                for imp in imports:
                    if imp["name"] not in name_names:
                        imp.update(path=file)
                        print(imp)
