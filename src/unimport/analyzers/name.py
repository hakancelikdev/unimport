import ast

from unimport import constants as C
from unimport import typing as T
from unimport.analyzers.decarators import generic_visit
from unimport.analyzers.utils import first_parent_match, get_parents, set_tree_parents
from unimport.statement import Name, Scope

__all__ = ("NameAnalyzer",)


class NameAnalyzer(ast.NodeVisitor):
    def visit_ClassDef(self, node) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    def visit_FunctionDef(self, node: T.ASTFunctionT) -> None:
        Scope.add_current_scope(node)

        self._type_comment(node)
        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_str_helper(self, value: str, node: ast.AST) -> None:
        parent = first_parent_match(node, *C.AST_FUNCTION_TUPLE)
        is_annassign_or_arg = any(isinstance(parent, (ast.AnnAssign, ast.arg)) for parent in get_parents(node))
        if is_annassign_or_arg or (parent is not None and parent.returns is node):
            self.join_visit(value, node)

    def visit_Str(self, node: ast.Str) -> None:
        self.visit_str_helper(node.s, node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str):
            self.visit_str_helper(node.value, node)

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
        self._type_comment(node)

    @generic_visit
    def visit_arg(self, node: ast.arg) -> None:
        self._type_comment(node)

    @generic_visit
    def visit_Subscript(self, node: ast.Subscript) -> None:
        # type_variable
        # type_var = List["object"] etc.

        def visit_constant_str(node: T.ASTNameType) -> None:
            """Separates the value by node type (str or constant) and gives it
            to the visit function."""

            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                self.join_visit(node.value, node)
            elif isinstance(node, ast.Str):
                self.join_visit(node.s, node)

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
                    if isinstance(elt, (ast.Constant, ast.Str)):
                        visit_constant_str(elt)
            else:
                if isinstance(_slice, (ast.Constant, ast.Str)):  # type: ignore
                    visit_constant_str(_slice)  # type: ignore

    @generic_visit
    def visit_Call(self, node: ast.Call) -> None:
        # type_variable
        # cast("type", return_value)
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
            elif isinstance(node.args[0], ast.Str):
                self.join_visit(node.args[0].s, node.args[0])

    def _type_comment(self, node: ast.AST) -> None:
        mode = "func_type" if isinstance(node, C.AST_FUNCTION_TUPLE) else "eval"
        type_comment = getattr(node, "type_comment", None)
        if type_comment is not None:
            self.join_visit(type_comment, node, mode=mode)

    def join_visit(self, value: str, node: ast.AST, *, mode: str = "eval") -> None:
        """A function that parses the value, copies locations from the node and
        includes them in self.visit."""
        try:
            tree = ast.parse(value, mode=mode, type_comments=True) if C.PY38_PLUS else ast.parse(value, mode=mode)
        except SyntaxError:
            return None
        else:
            set_tree_parents(tree, parent=node.parent)  # type: ignore
            for new_node in ast.walk(tree):
                ast.copy_location(new_node, node)
            self.visit(tree)

    def traverse(self, tree) -> None:
        self.visit(tree)
