from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import syms, token
from lib2to3.refactor import RefactoringTool


def traverse_imports(names):
    pending = [names]
    while pending:
        node = pending.pop()
        if node.type == token.NAME:
            yield node.value
        elif node.type == syms.dotted_name:
            yield "".join([ch.value for ch in node.children])
        elif node.type == syms.dotted_as_name:
            pending.append(node.children[0])
        elif node.type in {syms.dotted_as_names, syms.import_as_names}:
            pending.extend(node.children[::-2])
        else:
            raise ValueError("unknown node type", node.type)


class RefactorImports(BaseFix):
    PATTERN = """
    import_from< 'from' imp=any 'import' ['('] items=any [')'] >
    |
    import_name< 'import' imp=any >
    """

    def __init__(self, unused_modules):
        self.unused_modules = unused_modules
        super().__init__(None, None)  # options and logger

    def transform(self, node, results):
        imports = results["imp"]

        if node.type == syms.import_from:
            if str(imports).strip() in self.unused_modules:
                node.parent.remove()
            else:
                self.transform_inner_body(node, results["items"])
        else:
            self.transform_inner_body(node, imports)

    def transform_inner_body(self, node, imports):
        if imports.children:
            body = imports.children
        else:
            body = [imports]

        def remove_comma():
            nonlocal trailing_comma
            if index + 1 == len(modules):
                comma = commas.pop(index - remove_counter - 1)
                if trailing_comma:
                    trailing_comma.remove()
                    trailing_comma = None
            else:
                comma = commas.pop(index - remove_counter)
            comma.remove()

        trailing_comma = None
        if body[-1].type == token.COMMA:
            trailing_comma = body.pop()

        commas = body[1:-1:2]
        module_nodes = body[::2]
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

        if trailing_comma:
            body.append(trailing_comma)


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
