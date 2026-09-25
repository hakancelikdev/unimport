from __future__ import annotations

import ast
import contextlib

from unimport import constants as C
from unimport import typing as T
from unimport.analyzers.decarators import generic_visit
from unimport.analyzers.utils import get_parents, set_tree_parents
from unimport.statement import Name, Scope

__all__ = ("NameAnalyzer",)

_TYPE_VAR_FACTORIES = frozenset({"TypeVar", "ParamSpec", "TypeVarTuple"})
# PEP 695 nodes exist from Python 3.12.
_TYPE_ALIAS = tuple(getattr(ast, name) for name in ("TypeAlias",) if hasattr(ast, name))
_TYPE_PARAMS = tuple(getattr(ast, name) for name in ("TypeVar", "ParamSpec", "TypeVarTuple") if hasattr(ast, name))


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
        if isinstance(node.value, str) and not self._is_typing_subscript_slice(node) and self._is_type_expression(node):
            self.join_visit(node.value, node)

    @staticmethod
    def _subscript_name(node: ast.Subscript) -> str | None:
        if isinstance(node.value, ast.Name):
            return node.value.id
        if isinstance(node.value, ast.Attribute):
            return node.value.attr
        return None

    @classmethod
    def _is_typing_subscript_slice(cls, node: ast.Constant) -> bool:
        """Strings that visit_Subscript already parses."""
        parent = node.parent  # type: ignore
        if isinstance(parent, ast.Tuple):
            parent = parent.parent  # type: ignore
        return isinstance(parent, ast.Subscript) and (
            (
                isinstance(parent.value, ast.Attribute)
                and isinstance(parent.value.value, ast.Name)
                and parent.value.value.id == "typing"
            )
            or (isinstance(parent.value, ast.Name) and parent.value.id in C.SUBSCRIPT_TYPE_VARIABLE)
        )

    @classmethod
    def _is_type_expression(cls, node: ast.AST) -> bool:
        """Whether a string constant is written where a type is expected.

        That is inside an annotation, a return annotation, the value of
        an ``X: TypeAlias = ...`` or a string that was itself parsed as a
        type. ``Literal[...]`` values and ``Annotated[...]`` metadata are
        not types.
        """
        child = node
        for parent in get_parents(node):
            if isinstance(parent, ast.Subscript) and child is parent.slice:
                name = cls._subscript_name(parent)
                if name == "Literal":
                    return False
            elif isinstance(parent, ast.Tuple) and isinstance(parent.parent, ast.Subscript):  # type: ignore
                if cls._subscript_name(parent.parent) == "Annotated" and child is not parent.elts[0]:  # type: ignore
                    return False
            elif isinstance(parent, (ast.Expression, ast.FunctionType)):  # a string parsed by join_visit
                return True
            elif isinstance(parent, ast.arg):
                return child is parent.annotation
            elif isinstance(parent, ast.AnnAssign):
                if child is parent.annotation:
                    return True
                return child is parent.value and cls._is_type_alias_annotation(parent.annotation)
            elif isinstance(parent, C.AST_FUNCTION_TUPLE):
                return child is parent.returns
            elif isinstance(parent, _TYPE_ALIAS):  # type X = "Y" (PEP 695)
                return child is parent.value  # type: ignore[attr-defined]
            elif isinstance(parent, _TYPE_PARAMS):  # def f[T: "Y" = "Z"]() (PEP 695 / 696)
                return child is getattr(parent, "bound", None) or child is getattr(parent, "default_value", None)
            elif isinstance(parent, (ast.stmt, ast.Lambda)):
                return False
            child = parent
        return False

    @staticmethod
    def _call_name(node: ast.Call) -> str | None:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    @staticmethod
    def _is_type_alias_annotation(annotation: ast.expr) -> bool:
        return (isinstance(annotation, ast.Name) and annotation.id == "TypeAlias") or (
            isinstance(annotation, ast.Attribute) and annotation.attr == "TypeAlias"
        )

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

            name = self._subscript_name(node)
            if name == "Literal":  # Literal["os"] holds values, not types
                return
            if isinstance(_slice, ast.Tuple):  # type: ignore
                # Annotated[T, "metadata", ...]: only the first element is a type.
                elts = _slice.elts[:1] if name == "Annotated" else _slice.elts  # type: ignore
                for elt in elts:
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
        elif (factory := self._call_name(node)) in _TYPE_VAR_FACTORIES:
            # TypeVar("T", "A", "B", bound="C", default="D"): constraints, bound and default (PEP 696) are types;
            # the first argument is the name. ParamSpec and TypeVarTuple only take a default.
            constraints = node.args[1:] if factory == "TypeVar" else []
            keywords = [keyword.value for keyword in node.keywords if keyword.arg in ("bound", "default")]
            for arg in [*constraints, *keywords]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    self.join_visit(arg.value, arg)

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
