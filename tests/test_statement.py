import ast

from unimport.statement import Name, Scope


def test_scope_lookup_uses_identity():
    """Two Name objects with the same fields in different scopes keep their own scope."""
    tree = ast.parse("def f(): pass")
    function = tree.body[0]
    try:
        Scope.add_global_scope(tree)
        Name.register(lineno=1, name="os", node=ast.Name("os"))
        Scope.add_current_scope(function)
        Name.register(lineno=1, name="os", node=ast.Name("os"))
        Scope.remove_current_scope()

        global_name, local_name = Name.names
        assert global_name == local_name  # dataclass equality compares fields only
        assert global_name.scope.node is tree
        assert local_name.scope.node is function
        assert Scope.get_global_scope().child_scopes == {local_name.scope}
    finally:
        Scope.remove_current_scope()
        Name.clear()
        Scope.clear()
