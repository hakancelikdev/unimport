from __future__ import annotations

import ast

import unimport.constants as C
import unimport.typing as T
from unimport.analyzers.decarators import generic_visit
from unimport.analyzers.utils import first_parent_match

__all__ = (
    "ImportableNameAnalyzer",
    "SuggestionNameAnalyzer",
)

from unimport.statement import Name, Scope


class ImportableNameAnalyzer(ast.NodeVisitor):
    __slots__ = ("importable_nodes",)

    def __init__(self) -> None:
        self.importable_nodes: list[ast.Constant] = []  # nodes on the __all__ list

    def traverse(self, tree):
        self.visit(tree)

    @generic_visit
    def visit_Assign(self, node: ast.Assign) -> None:
        if getattr(node.targets[0], "id", None) == "__all__" and isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
            for item in node.value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    self.importable_nodes.append(item)

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
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        self.importable_nodes.append(arg)

            elif node.value.func.attr == "extend":
                for arg in node.value.args:
                    if isinstance(arg, ast.List):
                        for item in arg.elts:
                            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                                self.importable_nodes.append(item)


class SuggestionNameAnalyzer(ast.NodeVisitor):
    __slots__ = ("suggestions_nodes",)

    def __init__(self) -> None:
        self.suggestions_nodes: list[T.ASTImportableT] = []  # nodes on the CFN

    def traverse(self, tree):
        self.visit(tree)

    @generic_visit
    def visit_def(self, node: T.CFNT) -> None:
        if not first_parent_match(node, C.DEF_TUPLE):
            self.suggestions_nodes.append(node)

    visit_ClassDef = visit_FunctionDef = visit_AsyncFunctionDef = visit_def

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
        for target in node.targets:  # we only get assigned names
            if isinstance(target, (ast.Name, ast.Attribute)):
                self.suggestions_nodes.append(target)


class ImportableNameWithScopeAnalyzer(ImportableNameAnalyzer):
    def traverse(self, tree):
        super().traverse(tree)

        for node in self.importable_nodes:
            Name.register(lineno=node.lineno, name=node.value, node=node, is_all=True)

    def visit_def(self, node: T.CFNT) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_ClassDef = visit_FunctionDef = visit_AsyncFunctionDef = visit_def
