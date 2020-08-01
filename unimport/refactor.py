from typing import List, Union

import libcst as cst

from unimport.color import Color
from unimport.statement import Import, ImportFrom


class RemoveUnusedImportTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = [cst.metadata.PositionProvider]

    def __init__(
        self, unused_imports: List[Union[Import, ImportFrom]]
    ) -> None:
        self.unused_imports = unused_imports

    @staticmethod
    def get_import_name_from_attr(attr_node: cst.Attribute) -> str:
        name = [attr_node.children[2].value]  # last value
        node = attr_node.children[0]
        while hasattr(node, "value"):
            if hasattr(node, "attr"):
                name.append(node.attr.value)
                node = node.value
            else:
                name.append(node.value)
                break
        name.reverse()
        return ".".join(name)

    def is_import_used(
        self, import_name: str, location: cst._position.CodeRange
    ) -> bool:
        return not any(
            imp.name == import_name and imp.lineno == location.start.line
            for imp in self.unused_imports
        )

    def get_location(
        self, node: Union[cst.Import, cst.ImportFrom]
    ) -> cst._position.CodeRange:
        return self.get_metadata(cst.metadata.PositionProvider, node)

    def leave_import_alike(
        self,
        original_node: Union[cst.Import, cst.ImportFrom],
        updated_node: Union[cst.Import, cst.ImportFrom],
    ) -> Union[cst.RemovalSentinel, cst.Import, cst.ImportFrom]:
        names_to_keep = []
        for import_alias in updated_node.names:
            if isinstance(import_alias.name, cst.Attribute):
                import_name = self.get_import_name_from_attr(
                    attr_node=import_alias.name
                )
            else:
                import_name = (import_alias.asname or import_alias).name.value
            if self.is_import_used(
                import_name, self.get_location(original_node)
            ):
                names_to_keep.append(import_alias)
        if not names_to_keep:
            return cst.RemoveFromParent()
        elif len(updated_node.names) == len(names_to_keep):
            return updated_node
        else:
            names_to_keep[-1] = names_to_keep[-1].with_changes(
                comma=cst.MaybeSentinel.DEFAULT
            )
            return updated_node.with_changes(names=names_to_keep)

    @staticmethod
    def leave_StarImport(
        original_node: cst.ImportFrom,
        updated_node: cst.ImportFrom,
        imp: ImportFrom,
    ) -> Union[cst.ImportFrom, cst.RemovalSentinel]:
        if imp.modules:
            names_to_suggestion = [
                cst.ImportAlias(cst.Name(module)) for module in imp.modules
            ]
            return updated_node.with_changes(names=names_to_suggestion)
        elif imp.module:
            return cst.RemoveFromParent()
        return original_node

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> Union[cst.RemovalSentinel, cst.Import]:
        return self.leave_import_alike(original_node, updated_node)

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> Union[cst.RemovalSentinel, cst.ImportFrom]:
        if isinstance(updated_node.names, cst.ImportStar):

            def get_star_imp():
                if isinstance(updated_node.module, cst.Attribute):
                    import_name = self.get_import_name_from_attr(
                        attr_node=updated_node.module
                    )
                else:
                    import_name = updated_node.module.value
                location = self.get_location(original_node)
                for imp in self.unused_imports:
                    if (
                        imp.name == import_name
                        and imp.lineno == location.start.line
                    ):
                        return imp

            imp = get_star_imp()
            if imp:
                return self.leave_StarImport(original_node, updated_node, imp)
            return original_node
        return self.leave_import_alike(original_node, updated_node)


def refactor_string(
    source: str,
    unused_imports: List[Union[Import, ImportFrom]],
    show_error: bool = False,
) -> str:
    try:
        wrapper = cst.MetadataWrapper(cst.parse_module(source))
    except cst.ParserSyntaxError as err:
        if show_error:
            print(Color(str(err)).red)
    else:
        if unused_imports:
            fixed_module = wrapper.visit(
                RemoveUnusedImportTransformer(unused_imports)
            )
            return fixed_module.code
    return source
