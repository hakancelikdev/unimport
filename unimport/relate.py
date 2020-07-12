# https://tree.science/using-ancestral-chains-in-ast.html

import ast


def relate(tree):
    tree.parent = None
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent


def get_parents(node):
    parent = node
    while parent:
        parent = parent.parent
        yield parent


def first_occurrence(node, *ancestors):
    for parent in get_parents(node):
        if type(parent) in ancestors:
            return parent
    else:
        return False
