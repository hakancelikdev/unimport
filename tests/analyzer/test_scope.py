import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Scope


def test_names():
    source = textwrap.dedent(
        """
        import y as x
        import x

        def func(p=x):
            tt = 0

        import x
        x
        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2

        names = Scope.scopes[0].names

        name = next(names)
        assert name.name == "x"
        assert name.lineno == 9

        name = next(names)
        assert name.name == "x"
        assert name.lineno == 5

        name = next(names)
        assert name.name == "tt"
        assert name.lineno == 6

        imports = Scope.scopes[0].imports

        _import = next(imports)
        assert _import.is_duplicate is True
        assert _import.lineno == 2
        assert _import.is_used() is False

        _import = next(imports)
        assert _import.is_duplicate is True
        assert _import.lineno == 3
        assert _import.is_used() is True

        _import = next(imports)
        assert _import.is_duplicate is True
        assert _import.lineno == 8
        assert _import.is_used() is True


def test_import_module_scope():
    source = textwrap.dedent(
        """
        import x

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 1
        assert Scope.scopes[0].parent is None
        assert Scope.scopes[0].child_scopes == set()


def test_import_class_scope():
    source = textwrap.dedent(
        """
        class Klass:
            import x

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2
        assert Scope.scopes[1].parent == Scope.get_global_scope()
        assert Scope.scopes[1].parent.parent is None
        assert Scope.scopes[1].node.name == "Klass"
        assert Scope.scopes[0].child_scopes.pop() == Scope.scopes[1]


def test_import_function_scope():
    source = textwrap.dedent(
        """
        def func():
            import x

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2
        assert Scope.scopes[1].parent.parent is None
        assert Scope.scopes[1].node.name == "func"
        assert Scope.scopes[0].child_scopes.pop() == Scope.scopes[1]


def test_import_nonlocal_scope():
    source = textwrap.dedent(
        """
        def func():
            def inner():
                import x

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 3
        assert Scope.scopes[1].parent.parent.parent is None
        assert Scope.scopes[1].parent.node.name == "func"
        assert Scope.scopes[1].node.name == "inner"
        assert Scope.scopes[1].current_nodes.pop().name == "x"
        assert Scope.scopes[0].child_scopes.pop() == Scope.scopes[1].parent


def test_name_global_scope():
    source = textwrap.dedent(
        """
        x = 1

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 1
        assert Scope.scopes[0].parent is None
        assert Scope.scopes[0].current_nodes[0].name == "x"


def test_name_class_scope():
    source = textwrap.dedent(
        """
        class Klass:
            x = 1

            """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2
        assert Scope.scopes[1].parent.parent is None
        assert Scope.scopes[1].node.name == "Klass"
        assert Scope.scopes[1].current_nodes[0].name == "x"


def test_name_function_scope():
    source = textwrap.dedent(
        """
        def func():
            x = 1

            """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2
        assert Scope.scopes[1].parent.parent is None
        assert Scope.scopes[1].node.name == "func"
        assert Scope.scopes[1].current_nodes[0].name == "x"


def test_name_nonlocal_scope():
    source = textwrap.dedent(
        """
        def func():
            def inner():
                x = 1

            """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 3
        assert Scope.scopes[1].parent.parent.parent is None
        assert Scope.scopes[1].parent.node.name == "func"
        assert Scope.scopes[1].current_nodes[0].name == "x"


def test_name_and_import_module_scope():
    source = textwrap.dedent(
        """
        import global_import_x

        def func():
            import local_import_x

            loca_name_x

        global_name_x

            """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 2
        assert Scope.scopes[1].parent.parent is None
        assert len(Scope.scopes[1].current_nodes) == 2
        assert Scope.scopes[0].current_nodes[1].name == "global_import_x"
        assert Scope.scopes[0].current_nodes[0].name == "global_name_x"

        assert Scope.scopes[1].parent == Scope.scopes[0]
        assert Scope.scopes[1].node.name == "func"
        assert Scope.scopes[1].current_nodes[1].name == "local_import_x"
        assert Scope.scopes[1].current_nodes[0].name == "loca_name_x"


def test_global_loca_inner_scope():
    source = textwrap.dedent(
        """
        import x

        def func():
            import x

            def inner():
                import x
                x

            x

        x

        """
    )

    with Analyzer(source=source):
        assert len(Scope.scopes) == 3
        assert Scope.scopes[0].parent is None
        assert Scope.scopes[2].parent.parent is None
        assert Scope.scopes[1].parent.parent.parent is None

        assert len(list(Scope.scopes[1].names)) == 1
        assert list(Scope.scopes[1].names)[0].lineno == 9
        assert len(list(Scope.scopes[2].names)) == 2
        assert list(Scope.scopes[2].names)[0].lineno == 11
        assert len(list(Scope.scopes[0].names)) == 3
