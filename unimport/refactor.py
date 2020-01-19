from contextlib import contextmanager
from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import BlankLine, syms, token
from lib2to3.refactor import RefactoringTool


def traverse_imports(names):
    pending = [names]
    while pending:
        node = pending.pop()
        if node.type == token.NAME:
            yield node.value
        elif node.type == syms.dotted_name:
            yield "".join([ch.value for ch in node.children])
        elif node.type in {syms.dotted_as_name, syms.import_as_name}:
            pending.append(node.children[0])
        elif node.type in {syms.dotted_as_names, syms.import_as_names}:
            pending.extend(node.children[::-2])
        else:
            raise ValueError("unknown node type", node.type)


class RefactorImports(BaseFix):

    PATTERN = r"""
        simple_stmt<
            (
                import_name< 'import' imp=any >
                |
                import_from< 'from' imp=['.'*] any 'import' ['('] items=any [')'] >
            ) '\n'
        >
    """

    def __init__(self):
        self.unused_modules = []
        super().__init__(None, None)  # options and logger

    @contextmanager
    def clean(self, unused_modules):
        try:
            self.unused_modules.clear()
            self.unused_modules.extend(unused_modules)
            yield
        finally:
            self.unused_modules.clear()

    def transform(self, node, results):
        imports = results["imp"]
        if node.children[0].type == syms.import_from:
            if str(imports).strip() in self.unused_modules:
                return BlankLine()
            else:
                return self.transform_inner_body(
                    node, results["items"], from_import=True
                )
        else:
            return self.transform_inner_body(node, imports)

    def transform_inner_body(self, node, imports, from_import=False):
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
            return BlankLine()

        if trailing_comma:
            body.append(trailing_comma)


class RefactorTool(RefactoringTool):
    def __init__(self):
        self._fixer = RefactorImports()
        self._fixers = [self._fixer]
        super().__init__(None, options = {"print_function": True})
        del self.grammar.keywords["exec"]

    def get_fixers(self):
        return self._fixers, []

    def refactor_string(self, source, unused_imports):
        with self._fixer.clean(unused_imports):
            source = super().refactor_string(source, "unimport")
        return str(source)
