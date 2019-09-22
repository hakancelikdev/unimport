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


def get_conf(directory):
    "Checks if there is a configuration file under the entered path and returns as a list."
    try:
        _unimport_conf = tokenize.open(
            os.path.join(
                os.getcwd(),
                directory,
                ".unimport.cfg"
            )
        ).readlines()
    except FileNotFoundError:
        return False
    else:
        return [conf.replace("\n", "") for conf in _unimport_conf]


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

    def get_diff(self):
        for imp in self.imports:
            len_dot = len(imp["name"].split("."))
            for name in self.names:
                if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                    break
            else:
                yield imp


def unimport():
    try:
        source_file_or_directory = sys.argv[1]
    except IndexError:
        print("No paths given 'Usage; unimport {source_file_or_directory}'")
    else:
        if os.path.isdir(source_file_or_directory):
            # folder
            conf = get_conf(directory=source_file_or_directory)
            for root, dirs, files in os.walk(sys.argv[1]):
                for name in files:
                    file_path = os.path.join(root, name)
                    if file_path.endswith(".py"):
                        if conf:
                            diff = set(file_path.split(os.sep)) - set(conf)
                            if diff != set(file_path.split(os.sep)):
                                continue
                        unimport = UnImport(source=tokenize.open(file_path).read())
                        for unused in unimport.get_diff():
                            unused.update(path=file_path.replace(os.getcwd(), ""))
                            print(unused)
        else:
            # file
            file_path = os.path.join(os.getcwd(), source_file_or_directory)
            if file_path.endswith(".py"):
                unimport = UnImport(source=tokenize.open(file_path).read())
                for unused in unimport.get_diff():
                    unused.update(path=file_path.replace(os.getcwd(), ""))
                    print(unused)

if __name__ == "__main__":
    # test
    import inspect

    unused_import = UnImport(source=inspect.getsource(os))
    for unused in unused_import.get_diff():
        print(unused)
