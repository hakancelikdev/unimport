import ast
import contextlib

from unimport import constants as C
from unimport import typing as T
from unimport.analyzers.decarators import generic_visit
from unimport.analyzers.utils import first_parent_match, set_tree_parents
from unimport.statement import Name, Scope

__all__ = ("NameAnalyzer",)


class NameAnalyzer(ast.NodeVisitor):
    def visit_ClassDef(self, node) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    def visit_FunctionDef(self, node: T.ASTFunctionT) -> None:
        Scope.add_current_scope(node)

        if node.type_comment is not None:
            self.join_visit(node.type_comment, node, mode="func_type")

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    @generic_visit
    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str):
            if (first_annassign_or_arg := first_parent_match(node, (ast.AnnAssign, ast.arg))) and isinstance(
                first_annassign_or_arg.annotation, ast.Constant
            ):
                self.join_visit(node.value, node)
            elif (
                first_func_parent := first_parent_match(node, *C.AST_FUNCTION_TUPLE)
            ) and first_func_parent.returns is node:
                self.join_visit(node.value, node)

    @generic_visit
    def visit_Name(self, node: ast.Name) -> None:
        if not isinstance(node.parent, ast.Attribute):  # type: ignore
            Name.register(lineno=node.lineno, name=node.id, node=node)

    @generic_visit
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if not isinstance(node.value, ast.Call):
            names = []
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Attribute):
                    names.append(sub_node.attr)
                elif isinstance(sub_node, ast.Name):
                    names.append(sub_node.id)
            names.reverse()
            Name.register(lineno=node.lineno, name=".".join(names), node=node)

    @generic_visit
    def visit_Assign(self, node: ast.Assign) -> None:
        if node.type_comment is not None:
            self.join_visit(node.type_comment, node)

    @generic_visit
    def visit_arg(self, node: ast.arg) -> None:
        if node.type_comment is not None:
            self.join_visit(node.type_comment, node)

    @generic_visit
    def visit_Subscript(self, node: ast.Subscript) -> None:
        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "typing"
        ) or (isinstance(node.value, ast.Name) and node.value.id in C.SUBSCRIPT_TYPE_VARIABLE):
            if C.PY39_PLUS:
                _slice = node.slice
            else:
                _slice = node.slice.value  # type: ignore

            if isinstance(_slice, ast.Tuple):  # type: ignore
                for elt in _slice.elts:  # type: ignore
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        self.join_visit(elt.value, elt)
            else:
                if isinstance(_slice, ast.Constant) and isinstance(_slice.value, str):  # type: ignore
                    self.join_visit(_slice.value, _slice)

    @generic_visit
    def visit_Call(self, node: ast.Call) -> None:
        if (
            (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "typing"
                and node.func.attr == "cast"
            )
            or isinstance(node.func, ast.Name)
            and node.func.id == "cast"
        ):
            if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                self.join_visit(node.args[0].value, node.args[0])

    def join_visit(self, value: str, node: ast.AST, *, mode: str = "eval") -> None:
        """A function that parses the value, copies locations from the node and
        includes them in self.visit."""
        with contextlib.suppress(SyntaxError):
            tree = ast.parse(value, mode=mode, type_comments=True)
            set_tree_parents(tree, parent=node.parent)  # type: ignore
            for new_node in ast.walk(tree):
                ast.copy_location(new_node, node)
            self.visit(tree)

    def traverse(self, tree) -> None:
        self.visit(tree)
