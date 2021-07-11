import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.statement import Scope


class ScopeAnalyzerTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        Scope.clear()

    def test_names(self):
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

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)

        names = Scope.scopes[0].names

        name = next(names)
        self.assertEqual(name.name, "x")
        self.assertEqual(name.lineno, 9)

        name = next(names)
        self.assertEqual(name.name, "x")
        self.assertEqual(name.lineno, 5)

        name = next(names)
        self.assertEqual(name.name, "tt")
        self.assertEqual(name.lineno, 6)

        imports = Scope.scopes[0].imports

        _import = next(imports)
        self.assertTrue(_import.is_duplicate)
        self.assertEqual(_import.lineno, 2)
        self.assertFalse(_import.is_used())

        _import = next(imports)
        self.assertTrue(_import.is_duplicate)
        self.assertEqual(_import.lineno, 3)
        self.assertTrue(_import.is_used())

        _import = next(imports)
        self.assertTrue(_import.is_duplicate)
        self.assertEqual(_import.lineno, 8)
        self.assertTrue(_import.is_used())

    def test_import_module_scope(self):
        source = textwrap.dedent(
            """
            import x

            """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 1)
        self.assertIsNone(Scope.scopes[0].parent)
        self.assertEqual(Scope.scopes[0].child_scopes, [])

    def test_import_class_scope(self):
        source = textwrap.dedent(
            """
            class Klass:
                import x

            """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertEqual(Scope.scopes[1].parent, Scope.get_global_scope())
        self.assertIsNone(Scope.scopes[1].parent.parent)
        self.assertEqual(Scope.scopes[1].node.name, "Klass")
        self.assertEqual(Scope.scopes[0].child_scopes[0], Scope.scopes[1])

    def test_import_function_scope(self):
        source = textwrap.dedent(
            """
            def func():
                import x

            """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent)
        self.assertEqual(Scope.scopes[1].node.name, "func")
        self.assertEqual(Scope.scopes[0].child_scopes[0], Scope.scopes[1])

    def test_import_nonlocal_scope(self):
        source = textwrap.dedent(
            """
            def func():
                def inner():
                    import x

            """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent.parent)
        self.assertEqual(Scope.scopes[1].parent.node.name, "func")
        self.assertEqual(Scope.scopes[1].node.name, "inner")
        self.assertEqual(Scope.scopes[1].current_nodes[0].name, "x")
        self.assertEqual(
            Scope.scopes[0].child_scopes[0], Scope.scopes[1].parent
        )
        self.assertEqual(
            Scope.scopes[0].child_scopes[0].child_scopes[0], Scope.scopes[1]
        )

    def test_name_global_scope(self):
        source = textwrap.dedent(
            """
            x = 1

            """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 1)
        self.assertIsNone(Scope.scopes[0].parent)
        self.assertEqual(Scope.scopes[0].current_nodes[0].name, "x")

    def test_name_class_scope(self):
        source = textwrap.dedent(
            """
            class Klass:
                x = 1

                """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent)
        self.assertEqual(Scope.scopes[1].node.name, "Klass")
        self.assertEqual(Scope.scopes[1].current_nodes[0].name, "x")

    def test_name_function_scope(self):
        source = textwrap.dedent(
            """
            def func():
                x = 1

                """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent)
        self.assertEqual(Scope.scopes[1].node.name, "func")
        self.assertEqual(Scope.scopes[1].current_nodes[0].name, "x")

    def test_name_nonlocal_scope(self):
        source = textwrap.dedent(
            """
            def func():
                def inner():
                    x = 1

                """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent.parent)
        self.assertEqual(Scope.scopes[1].parent.node.name, "func")
        self.assertEqual(Scope.scopes[1].current_nodes[0].name, "x")

    def test_name_and_import_module_scope(self):
        source = textwrap.dedent(
            """
            import global_import_x

            def func():
                import local_import_x

                loca_name_x

            global_name_x

                """
        )

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 2)
        self.assertIsNone(Scope.scopes[1].parent.parent)
        self.assertEqual(len(Scope.scopes[1].current_nodes), 2)
        self.assertEqual(
            Scope.scopes[0].current_nodes[1].name, "global_import_x"
        )
        self.assertEqual(
            Scope.scopes[0].current_nodes[0].name, "global_name_x"
        )

        self.assertEqual(Scope.scopes[1].parent, Scope.scopes[0])
        self.assertEqual(Scope.scopes[1].node.name, "func")
        self.assertEqual(
            Scope.scopes[1].current_nodes[1].name, "local_import_x"
        )
        self.assertEqual(Scope.scopes[1].current_nodes[0].name, "loca_name_x")

    def test_global_loca_inner_scope(self):
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

        Analyzer(source=source).traverse()

        self.assertEqual(len(Scope.scopes), 3)
        self.assertIsNone(Scope.scopes[0].parent)
        self.assertIsNone(Scope.scopes[1].parent.parent.parent)
        self.assertIsNone(Scope.scopes[2].parent.parent)
        self.assertEqual(1, len(list(Scope.scopes[1].names)))
        self.assertEqual(9, list(Scope.scopes[1].names)[0].lineno)
        self.assertEqual(2, len(list(Scope.scopes[2].names)))
        self.assertEqual(11, list(Scope.scopes[2].names)[0].lineno)
        self.assertEqual(3, len(list(Scope.scopes[0].names)))
