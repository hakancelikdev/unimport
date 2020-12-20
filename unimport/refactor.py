from typing import List, Optional, Sequence, TypeVar, Union, cast

import libcst as cst
import libcst.matchers as m
from libcst.metadata import CodeRange, PositionProvider

from unimport.statement import Import, ImportFrom

__all__ = ["refactor_string"]

ImportT = TypeVar("ImportT", bound=Union[cst.Import, cst.ImportFrom])


class _RemoveUnusedImportTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(
        self, unused_imports: List[Union[Import, ImportFrom]]
    ) -> None:
        self.unused_imports = unused_imports

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

    def is_import_used(
        self, import_name: str, column: int, location: CodeRange
    ) -> bool:
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

    def get_location(
        self, node: Union[cst.Import, cst.ImportFrom]
    ) -> CodeRange:
        return self.get_metadata(cst.metadata.PositionProvider, node)

    @staticmethod
    def get_rpar(
        rpar: Optional[cst.RightParen], location: CodeRange
    ) -> Optional[cst.RightParen]:
        if not rpar or location.start.line == location.end.line:
            return rpar
        else:
            return cst.RightParen(
                whitespace_before=cst.ParenthesizedWhitespace()
            )

    def leave_import_alike(
        self,
        original_node: ImportT,
        updated_node: ImportT,
    ) -> Union[cst.RemovalSentinel, ImportT]:
        names_to_keep = []
        names = cast(Sequence[cst.ImportAlias], updated_node.names)
        # already handled by leave_ImportFrom
        for column, import_alias in enumerate(names):
            if isinstance(import_alias.name, cst.Attribute):
                import_name = self.get_import_name_from_attr(
                    attr_node=import_alias.name
                )
            else:
                raw_import = import_alias.asname or import_alias
                raw_import_name = cst.ensure_type(raw_import.name, cst.Name)
                import_name = raw_import_name.value
            if self.is_import_used(
                import_name, column + 1, self.get_location(original_node)
            ):
                names_to_keep.append(import_alias)
        if not names_to_keep:
            return cst.RemoveFromParent()
        elif len(names) == len(names_to_keep):
            return updated_node
        else:
            names_to_keep[-1] = names_to_keep[-1].with_changes(
                comma=cst.MaybeSentinel.DEFAULT
            )
            return cast(
                ImportT, updated_node.with_changes(names=names_to_keep)
            )

    @staticmethod
    def leave_StarImport(
        updated_node: cst.ImportFrom,
        imp: ImportFrom,
    ) -> Union[cst.ImportFrom, cst.RemovalSentinel]:
        if imp.suggestions:
            names_to_suggestions = [
                cst.ImportAlias(cst.Name(module)) for module in imp.suggestions
            ]
            return updated_node.with_changes(names=names_to_suggestions)
        else:
            return cst.RemoveFromParent()

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> Union[cst.RemovalSentinel, cst.Import]:
        return self.leave_import_alike(original_node, updated_node)

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> Union[cst.RemovalSentinel, cst.ImportFrom]:
        if isinstance(updated_node.names, cst.ImportStar):

            def get_star_imp() -> Optional[ImportFrom]:
                if isinstance(updated_node.module, cst.Attribute):
                    import_name = self.get_import_name_from_attr(
                        attr_node=updated_node.module
                    )
                else:
                    import_name = updated_node.module.value
                location = self.get_location(original_node)
                for imp in self.unused_imports:
                    if (
                        isinstance(imp, ImportFrom)
                        and imp.name == import_name
                        and imp.lineno == location.start.line
                    ):
                        return imp
                else:
                    return None

            imp = get_star_imp()
            if imp:
                return self.leave_StarImport(updated_node, imp)
            else:
                return original_node
        rpar = self.get_rpar(
            updated_node.rpar, self.get_location(original_node)
        )
        return self.leave_import_alike(
            original_node, updated_node.with_changes(rpar=rpar)
        )


def refactor_string(
    source: str,
    unused_imports: List[Union[Import, ImportFrom]],
) -> str:
    if unused_imports:
        wrapper = cst.MetadataWrapper(cst.parse_module(source))
        fixed_module = wrapper.visit(
            _RemoveUnusedImportTransformer(unused_imports)
        )
        return fixed_module.code
    return source
