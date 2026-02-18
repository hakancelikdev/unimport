from __future__ import annotations

from collections.abc import Sequence
from typing import cast

import libcst as cst
import libcst.matchers as m
from libcst.metadata import CodeRange, PositionProvider

from unimport import typing as T
from unimport.statement import Import, ImportFrom

__all__ = ("refactor_string",)


class _RemoveUnusedImportTransformer(cst.CSTTransformer):
    __slots__ = ("unused_imports", "_nodes_to_remove", "_pending_lines", "_pending_lines_stack")

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, unused_imports: list[Import | ImportFrom]) -> None:
        super().__init__()

        self.unused_imports = unused_imports
        self._nodes_to_remove: set[int] = set()
        self._pending_lines: list[cst.EmptyLine] = []
        self._pending_lines_stack: list[list[cst.EmptyLine]] = []

    @staticmethod
    def get_import_name_from_attr(attr_node: cst.Attribute) -> str:
        name = [attr_node.attr.value]  # last value
        node = attr_node.value
        while m.matches(node, m.OneOf(m.Name(), m.Attribute())):
            if isinstance(node, cst.Attribute):
                name.append(node.attr.value)
                node = node.value
            else:
                name.append(cst.ensure_type(node, cst.Name).value)
                break
        name.reverse()
        return ".".join(name)

    def is_import_used(self, import_name: str, column: int, location: CodeRange) -> bool:
        for imp in self.unused_imports:
            if all(
                (
                    imp.name == import_name,
                    imp.lineno == location.start.line,
                    imp.column == column,
                )
            ):
                return False
        return True

    def get_location(self, node: cst.Import | cst.ImportFrom) -> CodeRange:
        return self.get_metadata(cst.metadata.PositionProvider, node)

    @staticmethod
    def get_rpar(rpar: cst.RightParen | None, location: CodeRange) -> cst.RightParen | None:
        if not rpar or location.start.line == location.end.line:
            return rpar
        else:
            return cst.RightParen(whitespace_before=cst.ParenthesizedWhitespace())

    def leave_import_alike(self, original_node: T.CSTImportT, updated_node: T.CSTImportT) -> T.CSTImportT:
        names_to_keep = []
        names = cast(Sequence[cst.ImportAlias], updated_node.names)
        # already handled by leave_ImportFrom
        for column, import_alias in enumerate(names):
            if isinstance(import_alias.name, cst.Attribute):
                if import_alias.asname:
                    import_name = import_alias.asname.name.value
                else:
                    import_name = self.get_import_name_from_attr(attr_node=import_alias.name)
            else:
                raw_import = import_alias.asname or import_alias
                raw_import_name = cst.ensure_type(raw_import.name, cst.Name)
                import_name = raw_import_name.value
            if self.is_import_used(import_name, column + 1, self.get_location(original_node)):
                names_to_keep.append(import_alias)
        if not names_to_keep:
            self._nodes_to_remove.add(id(original_node))
            return updated_node
        elif len(names) == len(names_to_keep):
            return updated_node
        else:
            names_to_keep[-1] = names_to_keep[-1].with_changes(comma=cst.MaybeSentinel.DEFAULT)
            if isinstance(updated_node, cst.ImportFrom):
                rpar = self.get_rpar(updated_node.rpar, self.get_location(original_node))
                updated_node = updated_node.with_changes(rpar=rpar)

            updated_node = updated_node.with_changes(names=names_to_keep)
            return cast(T.CSTImportT, updated_node)

    @staticmethod
    def leave_StarImport(updated_node: cst.ImportFrom, imp: ImportFrom) -> tuple[cst.ImportFrom, bool]:
        if imp.suggestions:
            names_to_suggestions = [cst.ImportAlias(cst.Name(module)) for module in imp.suggestions]
            return updated_node.with_changes(names=names_to_suggestions), False
        else:
            return updated_node, True

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.Import:
        return self.leave_import_alike(original_node, updated_node)

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        if isinstance(updated_node.names, cst.ImportStar):

            def get_star_imp() -> ImportFrom | None:
                if isinstance(updated_node.module, cst.Attribute):
                    import_name = self.get_import_name_from_attr(attr_node=updated_node.module)
                else:
                    import_name = updated_node.module.value
                location = self.get_location(original_node)
                for imp in self.unused_imports:
                    if isinstance(imp, ImportFrom) and imp.name == import_name and imp.lineno == location.start.line:
                        return imp
                else:
                    return None

            imp = get_star_imp()
            if imp:
                result, should_remove = self.leave_StarImport(updated_node, imp)
                if should_remove:
                    self._nodes_to_remove.add(id(original_node))
                return result
            else:
                return original_node

        return self.leave_import_alike(original_node, updated_node)

    def leave_SimpleStatementLine(
        self,
        original_node: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.SimpleStatementLine | cst.RemovalSentinel:
        # Check if any child import node was marked for removal
        should_remove = False
        for stmt in original_node.body:
            if id(stmt) in self._nodes_to_remove:
                should_remove = True
                break

        if should_remove:
            # Extract comment-bearing lines (and blank lines that precede them)
            # from leading_lines and stash them
            lines = list(updated_node.leading_lines)
            preserved: list[cst.EmptyLine] = []
            for i, line in enumerate(lines):
                if isinstance(line, cst.EmptyLine) and line.comment is not None:
                    # Also include blank lines immediately before this comment
                    j = i - 1
                    blank_prefix: list[cst.EmptyLine] = []
                    while j >= 0 and isinstance(lines[j], cst.EmptyLine) and lines[j].comment is None:
                        blank_prefix.append(lines[j])
                        j -= 1
                    blank_prefix.reverse()
                    preserved.extend(blank_prefix)
                    preserved.append(line)
            self._pending_lines.extend(preserved)
            return cst.RemoveFromParent()

        # If there are pending comment lines, prepend them to this statement
        if self._pending_lines:
            new_leading = list(self._pending_lines) + list(updated_node.leading_lines)
            self._pending_lines.clear()
            return updated_node.with_changes(leading_lines=new_leading)

        return updated_node

    # -- Compound statement scope isolation --
    # Push/pop pending lines so that nested statements don't consume
    # pending lines from the outer scope.

    def _push_pending(self) -> None:
        self._pending_lines_stack.append(self._pending_lines)
        self._pending_lines = []

    def _pop_and_apply(self, updated_node: cst.BaseCompoundStatement) -> cst.BaseCompoundStatement:
        self._pending_lines = self._pending_lines_stack.pop()
        if self._pending_lines:
            new_leading = list(self._pending_lines) + list(updated_node.leading_lines)
            self._pending_lines.clear()
            return updated_node.with_changes(leading_lines=new_leading)
        return updated_node

    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        self._push_pending()
        return True

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        self._push_pending()
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_If(self, node: cst.If) -> bool:
        self._push_pending()
        return True

    def leave_If(self, original_node: cst.If, updated_node: cst.If) -> cst.BaseStatement | cst.RemovalSentinel:
        if (
            self._is_type_checking_if(updated_node)
            and self._is_body_pass_only(updated_node.body)
            and updated_node.orelse is None
        ):
            self._pending_lines = self._pending_lines_stack.pop()
            return cst.RemoveFromParent()
        return self._pop_and_apply(updated_node)

    @staticmethod
    def _is_type_checking_if(node: cst.If) -> bool:
        if isinstance(node.test, cst.Name) and node.test.value == "TYPE_CHECKING":
            return True
        if isinstance(node.test, cst.Attribute) and node.test.attr.value == "TYPE_CHECKING":
            return True
        return False

    @staticmethod
    def _is_body_pass_only(body: cst.BaseSuite) -> bool:
        if not isinstance(body, cst.IndentedBlock):
            return False
        return all(
            isinstance(stmt, cst.SimpleStatementLine) and all(isinstance(s, cst.Pass) for s in stmt.body)
            for stmt in body.body
        )

    def visit_For(self, node: cst.For) -> bool:
        self._push_pending()
        return True

    def leave_For(self, original_node: cst.For, updated_node: cst.For) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_While(self, node: cst.While) -> bool:
        self._push_pending()
        return True

    def leave_While(self, original_node: cst.While, updated_node: cst.While) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_Try(self, node: cst.Try) -> bool:
        self._push_pending()
        return True

    def leave_Try(self, original_node: cst.Try, updated_node: cst.Try) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_TryStar(self, node: cst.TryStar) -> bool:
        self._push_pending()
        return True

    def leave_TryStar(
        self, original_node: cst.TryStar, updated_node: cst.TryStar
    ) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def visit_With(self, node: cst.With) -> bool:
        self._push_pending()
        return True

    def leave_With(self, original_node: cst.With, updated_node: cst.With) -> cst.BaseStatement | cst.RemovalSentinel:
        return self._pop_and_apply(updated_node)

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        if self._pending_lines:
            new_footer = list(updated_node.footer) + list(self._pending_lines)
            self._pending_lines.clear()
            return updated_node.with_changes(footer=new_footer)
        return updated_node


def refactor_string(source: str, unused_imports: list[Import | ImportFrom]) -> str:
    if unused_imports:
        wrapper = cst.MetadataWrapper(cst.parse_module(source))
        fixed_module = wrapper.visit(_RemoveUnusedImportTransformer(unused_imports))
        return fixed_module.code

    return source
