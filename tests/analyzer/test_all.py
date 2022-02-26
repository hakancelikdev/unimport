import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import


def test_from_import():
    source = """\
        from codeop import compile_command
        __all__ = ["compile_command"]
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []


def test_defined_top():
    source = """\
        __all__ = ["x"]
        import x
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []
