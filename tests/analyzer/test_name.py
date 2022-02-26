import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, Name


def test_names():
    source = """\
        variable = 1
        variable1 = 2
        class TestClass:
            pass
        def function():
            pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=1, name="variable"),
            Name(lineno=2, name="variable1"),
        ]


def test_names_with_import():
    source = """\
       variable = 1
       import os
       class TestClass():
          def test_function(self):
              pass
       def test_function():
          pass
       """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [Name(lineno=1, name="variable")]
        assert Import.imports == [
            Import(lineno=2, column=1, name="os", package="os")
        ]


def test_names_with_function():
    source = """\
        variable = 1
        def test():
           pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [Name(lineno=1, name="variable")]


def test_names_with_class():
    source = """\
        variable = 1
        def test_function():
           pass
        class test():
           def test_function():
               pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [Name(lineno=1, name="variable")]


def test_decator_in_class():
    source = """\
        class Test:
            def test(self):
                def test2():
                    return 'test2'
                return test2
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [Name(lineno=5, name="test2")]


def test_normal_name_all_defined_top():
    source = """\
        __all__ = ["x"]
        import x
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=1, name="__all__"),
            Name(lineno=1, name="x", is_all=True),
        ]
        assert Import.imports == [
            Import(lineno=2, column=1, name="x", package="x")
        ]
