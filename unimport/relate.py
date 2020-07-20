# https://tree.science/using-ancestral-chains-in-ast.html

import ast
from typing import Iterator


def relate(tree: ast.Module) -> None:
    tree.parent = None  # type: ignore
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent  # type: ignore


def get_parents(node: ast.AST) -> Iterator[ast.AST]:
    parent = node
    while parent:
        parent = parent.parent  # type: ignore
        if parent is None:
            continue
        yield parent


def first_occurrence(node: ast.AST, *ancestors):
    for parent in get_parents(node):
        if type(parent) in ancestors:
            return parent
    else:
        return False
