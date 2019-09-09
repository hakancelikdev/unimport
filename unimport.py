import ast

class UnImport(ast.NodeVisitor):

    def __init__(self, source):
        self.imports = set()
        self.names = set()
        self.visit(ast.parse(source=source))

    def recursive(func):
        """ decorator to make visitor work recursive """
        def wrapper(self, node):
            func(self, node)
            for child in ast.iter_child_nodes(node):
                self.visit(child)
        return wrapper

    @recursive
    def visit_Import(self, node):
        for names in node.names:
            self.imports.add(names.name)
    @recursive
    def visit_ImportFrom(self, node):
        for names in node.names:
            self.imports.add(names.name)

    @recursive
    def visit_Name(self, node):
        self.names.add(node.id)

    @recursive
    def visit_Attribute(self, node):
        try:
            if self.imports.__contains__(f"{node.value.value.id}.{node.value.attr}"):
                self.names.add(f"{node.value.value.id}.{node.value.attr}")
        except AttributeError:
            pass


def unimport():
    import os
    import sys
    for root, dirs, files in os.walk(sys.argv[1]):
       for name in files:
          file = os.path.join(root, name)
          if file.endswith(".py"):
              unim = UnImport(source=open(file, "r", encoding="utf-8").read())
              names = unim.names
              imports = unim.imports
              for import_ in imports:
                  if import_ not in names:
                      print(f"File={file}, Module={import_}")
