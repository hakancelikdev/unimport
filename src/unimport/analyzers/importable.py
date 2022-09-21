import ast
from typing import FrozenSet, List

from unimport import constants as C
from unimport import typing as T
from unimport import utils
from unimport.analyzers.decarators import generic_visit
from unimport.analyzers.utils import first_parent_match, set_tree_parents
from unimport.statement import Name, Scope

__all__ = ("ImportableAnalyzer",)


class ImportableAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "importable_nodes",
        "suggestions_nodes",
    )

    def __init__(self) -> None:
        self.importable_nodes: List[T.ASTNameType] = []  # nodes on the __all__ list
        self.suggestions_nodes: List[T.ASTImportableT] = []  # nodes on the CFN

    def traverse(self, tree):
        self.visit(tree)

        for node in self.importable_nodes:
            if isinstance(node, ast.Constant):
                Name.register(lineno=node.lineno, name=str(node.value), node=node, is_all=True)
            elif isinstance(node, ast.Str):
                Name.register(lineno=node.lineno, name=node.s, node=node, is_all=True)

        self.clear()

    def visit_CFN(self, node: T.CFNT) -> None:
        Scope.add_current_scope(node)

        if not first_parent_match(node, C.DEF_TUPLE):
            self.suggestions_nodes.append(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_ClassDef = visit_CFN
    visit_FunctionDef = visit_CFN
    visit_AsyncFunctionDef = visit_CFN

    @generic_visit
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.suggestions_nodes.append(alias)

    @generic_visit
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if not node.names[0].name == "*":
            for alias in node.names:
                self.suggestions_nodes.append(alias)

    @generic_visit
    def visit_Assign(self, node: ast.Assign) -> None:
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
            for item in node.value.elts:
                if isinstance(item, (ast.Constant, ast.Str)):
                    self.importable_nodes.append(item)

        for target in node.targets:  # we only get assigned names
            if isinstance(target, (ast.Name, ast.Attribute)):
                self.suggestions_nodes.append(target)

    @generic_visit
    def visit_Expr(self, node: ast.Expr) -> None:
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and isinstance(node.value.func.value, ast.Name)
            and node.value.func.value.id == "__all__"
        ):
            if node.value.func.attr == "append":
                for arg in node.value.args:
                    if isinstance(arg, (ast.Constant, ast.Str)):
                        self.importable_nodes.append(arg)

            elif node.value.func.attr == "extend":
                for arg in node.value.args:
                    if isinstance(arg, ast.List):
                        for item in arg.elts:
                            if isinstance(item, (ast.Constant, ast.Str)):
                                self.importable_nodes.append(item)

    @classmethod
    def get_names(cls, package: str) -> FrozenSet[str]:
        if utils.is_std(package):
            return utils.get_dir(package)

        source = utils.get_source(package)
        if source:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                return frozenset()
            else:
                visitor = cls()
                set_tree_parents(tree)
                visitor.visit(tree)
                return visitor.get_all() or visitor.get_suggestion()
        return frozenset()

    def get_all(self) -> FrozenSet[str]:
        names = set()
        for node in self.importable_nodes:
            if isinstance(node, ast.Constant):
                names.add(node.value)
            elif isinstance(node, ast.Str):
                names.add(node.s)
        return frozenset(names)

    def get_suggestion(self) -> FrozenSet[str]:
        names = set()
        for node in self.suggestions_nodes:  # type: ignore
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.alias):
                names.add(node.asname or node.name)
            elif isinstance(node, C.DEF_TUPLE):
                names.add(node.name)
        return frozenset(names)

    def clear(self):
        self.importable_nodes.clear()
        self.suggestions_nodes.clear()
