import ast
from typing import Iterator, Optional

__all__ = ["relate", "get_parents", "first_occurrence"]


def relate(tree: ast.AST, parent: Optional[ast.AST] = None) -> None:
    tree.parent = parent  # type: ignore
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore


def get_parents(node: ast.AST) -> Iterator[ast.AST]:
    parent = node
    while parent:
        parent = parent.parent  # type: ignore
        if parent:
            yield parent


def first_occurrence(node: ast.AST, *ancestors):
    for parent in get_parents(node):
        if isinstance(parent, ancestors):
            return parent
    else:
        return None
