import ast
from typing import Set

from unimport import typing as T
from unimport.analyzers.decarators import generic_visit

__all__ = ("DefinedNameAnalyzer",)


class DefinedNameAnalyzer(ast.NodeVisitor):
    __slots__ = ("defined_names",)

    def __init__(self):
        self.defined_names: Set[str] = set()

    @generic_visit
    def visit_FunctionDef(self, node: T.ASTFunctionT) -> None:
        self.defined_names.add(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    @generic_visit
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.defined_names.add(node.name)

    @generic_visit
    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
