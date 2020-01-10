from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import syms
from lib2to3.fixes.fix_import import traverse_imports
from lib2to3.refactor import RefactoringTool


class RefactorImports(BaseFix):
    PATTERN = """
    import_from< 'from' imp=any 'import' ['('] any [')'] >
    |
    import_name< 'import' imp=any >
    """

    def __init__(self, unused_modules):
        self.unused_modules = unused_modules
        super().__init__(None, None)  # options and logger

    def transform(self, node, results):
        imports = results["imp"]  # the module or the modules

        def remove_comma():
            if index + 1 == len(modules):
                comma = commas.pop(index - remove_counter - 1)
            else:
                comma = commas.pop(index - remove_counter)
            comma.remove()

        if node.type == syms.import_from:
            if str(imports).strip() in self.unused_modules:
                node.parent.remove()
        else:
            body = imports if imports.children else node
            commas = body.children[1:-1:2]
            module_nodes = body.children[::2]
            modules = tuple(traverse_imports(imports))
            remove_counter = 0

            for index, module in enumerate(modules):
                if module in self.unused_modules:
                    if commas:
                        remove_comma()

                    module_nodes.pop(index - remove_counter).remove()
                    remove_counter += 1

            if remove_counter == len(modules):
                node.parent.remove()


class SingleRefactorer(RefactoringTool):
    def __init__(self, fixer):
        self._fixers = [fixer]
        super().__init__(None)

    def get_fixers(self):
        return self._fixers, []


def refactor(source, unused_modules):
    fixer = RefactorImports(unused_modules)
    refactorer = SingleRefactorer(fixer)
    return str(refactorer.refactor_string(source, "unimport"))
