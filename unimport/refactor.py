from contextlib import contextmanager
from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import (
    BlankLine, FromImport, Leaf, Newline, syms, token)
from lib2to3.refactor import RefactoringTool


def traverse_imports(names):
    """
    Walks over all the names imported in a dotted_as_names node.
    """
    pending = [names]
    while pending:
        node = pending.pop()
        if node.type in {token.NAME, token.STAR}:
            yield node.value
        elif node.type == syms.dotted_name:
            yield "".join([ch.value for ch in node.children])
        elif node.type in {syms.dotted_as_name, syms.import_as_name}:
            yield node.children[2].value
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
                import_from< 'from' imp=(['.'*] any) 'import' ['('] items=any [')'] >
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
        imp = self.get_imp_if_equal_to_lineno(node.get_lineno())
        if imp:
            if node.children[0].type == syms.import_from:
                return self.import_from(node, results, imp)
            elif node.children[0].type == syms.import_name:
                return self.import_name(node, results)

    def import_from(self, node, results, imp):
        if imp["star"] and imp["module"]:
            if not imp["modules"]:
                return BlankLine()
            else:
                package_name = imp["module"].__name__
                name_leafs = [
                    Leaf(
                        token.NAME,
                        ", ".join(sorted(imp["modules"])),
                        prefix=" ",
                    ),
                    Newline(),
                ]
                return FromImport(package_name, name_leafs)
        return self.transform_inner_children(node, results["items"])

    def import_name(self, node, results):
        return self.transform_inner_children(node, results["imp"])

    def get_imp_if_equal_to_lineno(self, lineno):
        for imp in self.unused_modules:
            if imp["lineno"] == lineno:
                return imp

    def transform_inner_children(self, node, imports):
        if imports.type == syms.import_as_name or not imports.children:
            children = [imports]
        else:
            children = imports.children
        trailing_comma = None
        if children[-1].type == token.COMMA:
            # if end of children's char is equal to ',' then remove it
            trailing_comma = children.pop()
        commas = children[1:-1:2]
        module_nodes = children[::2]
        modules = tuple(traverse_imports(imports))
        remove_counter = 0
        for index, module in enumerate(modules):
            if self.is_module_unused(module, node):
                if commas:
                    if index + 1 == len(modules):
                        comma = commas.pop(index - remove_counter - 1)
                        if trailing_comma:
                            trailing_comma.remove()
                            trailing_comma = None
                    else:
                        comma = commas.pop(index - remove_counter)
                    comma.remove()
                module_nodes.pop(index - remove_counter).remove()
                remove_counter += 1
        if remove_counter == len(modules):
            return BlankLine()
        if trailing_comma:
            children.append(trailing_comma)

    def is_module_unused(self, import_name, node):
        for imp in self.unused_modules:
            if (
                imp["name"] == import_name
                and imp["lineno"] == node.get_lineno()
            ):
                return imp


class RefactorTool(RefactoringTool):
    def __init__(self):
        self._fixer = RefactorImports()
        self._fixers = [self._fixer]
        super().__init__(None, options={"print_function": True})

    def get_fixers(self):
        return self._fixers, []

    def refactor_string(self, data, unused_imports, name="unimport"):
        with self._fixer.clean(unused_imports):
            source = super().refactor_string(data, name)
        return str(source)
