import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

from unimport.color import Color


class RemoveUnusedImportTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = [PositionProvider]

    def __init__(self, unused_imports):
        self.unused_imports = unused_imports

    @staticmethod
    def get_import_name_from_attr(attr_node):
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

    def is_import_used(self, import_name, location):
        return not any(
            [
                imp["name"] == import_name
                and imp["lineno"] == location.start.line
                for imp in self.unused_imports
            ]
        )

    def get_imp(self, import_name, location):
        for imp in self.unused_imports:
            if (
                imp["name"] == import_name
                and imp["lineno"] == location.start.line
            ):
                return imp

    def get_location(self, node):
        return self.get_metadata(PositionProvider, node)

    def leave_import_alike(self, original_node, updated_node):
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
                names_to_keep.append(
                    import_alias.with_changes(comma=cst.MaybeSentinel.DEFAULT)
                )
        if len(names_to_keep) == 0:
            return cst.RemoveFromParent()
        else:
            return updated_node.with_changes(names=names_to_keep)

    def leave_StarImport(self, original_node, updated_node, **kwargs):
        imp = kwargs["imp"]
        if imp["modules"]:
            modules = ",".join(imp["modules"])
            names_to_suggestion = []
            for module in modules.split(","):
                names_to_suggestion.append(cst.ImportAlias(cst.Name(module)))
            return updated_node.with_changes(names=names_to_suggestion)
        else:
            if imp["module"]:
                return cst.RemoveFromParent()
        return original_node

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> cst.Import:
        return self.leave_import_alike(original_node, updated_node)

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        if isinstance(updated_node.names, cst.ImportStar):

            def get_star_imp():
                if isinstance(updated_node.module, cst.Attribute):
                    import_name = self.get_import_name_from_attr(
                        attr_node=updated_node.module
                    )
                else:
                    import_name = updated_node.module.value
                return self.get_imp(
                    import_name=import_name,
                    location=self.get_location(original_node),
                )

            imp = get_star_imp()
            if imp:
                return self.leave_StarImport(
                    original_node, updated_node, imp=imp
                )
            return original_node
        return self.leave_import_alike(original_node, updated_node)


def refactor_string(source, unused_imports):
    try:
        wrapper = MetadataWrapper(cst.parse_module(source))
    except cst.ParserSyntaxError as err:
        print(Color(str(err)).red)
    else:
        if unused_imports:
            fixed_module = wrapper.visit(
                RemoveUnusedImportTransformer(unused_imports)
            )
            return fixed_module.code
    return source
