import ast
from typing import Iterator


class Relate:
    # https://tree.science/using-ancestral-chains-in-ast.html

    def __init__(self, tree: ast.AST) -> None:
        tree.parent = None  # type: ignore
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child.parent = parent  # type: ignore

    @classmethod
    def get_parents(cls, node: ast.AST) -> Iterator[ast.AST]:
        parent = node
        while parent:
            parent = parent.parent  # type: ignore
            if parent is None:
                continue
            yield parent

    @classmethod
    def first_occurrence(cls, node: ast.AST, *ancestors):
        for parent in cls.get_parents(node):
            if type(parent) in ancestors:
                return parent
        else:
            return False
