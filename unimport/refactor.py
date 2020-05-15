import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider


class RemoveUnusedImportTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, scanner):
        self.scanner = scanner
        self.unused_imports = list(self.scanner.get_unused_imports())
        self.imports = self.scanner.imports

    def get_import_name_from_attr(self, attr_node):
        module_attr = []
        children = attr_node.children
        module_attr.append(children[2].value)  # last value
        node_value = children[0]
        while True:
            if hasattr(node_value, "attr"):
                module_attr.append(node_value.attr.value)
                if hasattr(node_value, "value"):  # get parent
                    node_value = node_value.value
                else:
                    module_attr.append(node_value.value.value)
                    break
            else:
                module_attr.append(node_value.value)
                break
        module_attr.reverse()
        return ".".join(module_attr)

    def is_import_used(self, import_name, location):
        for imp in self.unused_imports:
            if (
                imp["name"] == import_name
                and imp["lineno"] == location.start.line
            ):
                # unused
                return False
        return True

    def get_imp(self, import_name, location):
        for imp in self.imports:
            if (
                imp["name"] == import_name
                and imp["lineno"] == location.start.line
            ):
                return imp

    def get_location(self, node):
        return self.get_metadata(PositionProvider, node)

    def leave_import_alike(self, original_node, updated_node):
        location = self.get_location(original_node)
        if isinstance(updated_node.names, cst.ImportStar):
            if isinstance(updated_node.module, cst.Attribute):
                import_name = self.get_import_name_from_attr(
                    attr_node=updated_node.module
                )
            else:
                import_name = updated_node.module.value
            imp = self.get_imp(import_name=import_name, location=location)
            if imp["modules"]:
                modules = ",".join(imp["modules"])
                names_to_suggestion = []
                for module in modules.split(","):
                    names_to_suggestion.append(
                        cst.ImportAlias(cst.Name(module))
                    )
                return updated_node.with_changes(names=names_to_suggestion)
            else:
                if imp["module"]:
                    return cst.RemoveFromParent()
        else:
            names_to_keep = []
            for import_alias in updated_node.names:
                if isinstance(import_alias.name, cst.Attribute):
                    import_name = self.get_import_name_from_attr(
                        attr_node=import_alias.name
                    )
                else:
                    import_name = (
                        import_alias.asname or import_alias
                    ).name.value
                if self.is_import_used(import_name, location):
                    names_to_keep.append(
                        import_alias.with_changes(
                            comma=cst.MaybeSentinel.DEFAULT
                        )
                    )
            if len(names_to_keep) == 0:
                return cst.RemoveFromParent()
            else:
                return updated_node.with_changes(names=names_to_keep)
        return updated_node

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> cst.Import:
        return self.leave_import_alike(original_node, updated_node)

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        return self.leave_import_alike(original_node, updated_node)


def refactor_string(scanner):
    try:
        wrapper = MetadataWrapper(cst.parse_module(scanner.source))
    except cst.ParserSyntaxError as err:
        print(f"\n\033[91m '{err}' \033[00m")
        return scanner.source
    fixed_module = wrapper.visit(RemoveUnusedImportTransformer(scanner))
    return fixed_module.code
