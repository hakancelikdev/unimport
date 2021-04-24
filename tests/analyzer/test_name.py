from tests.analyzer.utils import AnalyzerTestCase
from unimport.statement import Import, Name


class NameTestCase(AnalyzerTestCase):
    def test_names(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            variable1 = 2
            class TestClass:
               pass
            def function():
               pass
            """,
            expected_names=[
                Name(lineno=1, name="variable"),
                Name(lineno=2, name="variable1"),
            ],
        )

    def test_names_with_import(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            import os
            class TestClass():
               def test_function(self):
                   pass
            def test_function():
               pass
            """,
            expected_names=[Name(lineno=1, name="variable")],
            expected_imports=[
                Import(lineno=2, column=1, name="os", package="os")
            ],
        )

    def test_names_with_function(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            def test():
               pass
            """,
            expected_names=[Name(lineno=1, name="variable")],
        )

    def test_names_with_class(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            def test_function():
               pass
            class test():
               def test_function():
                   pass
            """,
            expected_names=[Name(lineno=1, name="variable")],
        )

    def test_decator_in_class(self):
        self.assertUnimportEqual(
            source="""\
            class Test:
                def test(self):
                    def test2():
                        return 'test2'
                    return test2
            """,
            expected_names=[Name(lineno=5, name="test2")],
        )

    def test_normal_name_all_defined_top(self):
        self.assertUnimportEqual(
            source="""\
            __all__ = ["x"]
            import x
            """,
            expected_names=[
                Name(lineno=1, name="__all__"),
                Name(lineno=1, name="x", is_all=True),
            ],
            expected_imports=[
                Import(lineno=2, column=1, name="x", package="x")
            ],
        )
