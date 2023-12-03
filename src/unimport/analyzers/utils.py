from __future__ import annotations

import ast
import typing

__all__ = ("set_tree_parents", "get_parents", "first_parent_match", "get_defined_names")


def set_tree_parents(tree: ast.AST, parent: ast.AST | None = None) -> None:
    tree.parent = parent  # type: ignore
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore


def get_parents(node: ast.AST) -> typing.Iterator[ast.AST]:
    parent = node
    while parent:
        parent = parent.parent  # type: ignore
        if parent:
            yield parent


def first_parent_match(node: ast.AST, *ancestors):
    return next(filter(lambda parent: isinstance(parent, ancestors), get_parents(node)), None)


def get_defined_names(tree: ast.AST) -> set[str]:
    defined_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined_names.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined_names.add(node.id)

    return defined_names
