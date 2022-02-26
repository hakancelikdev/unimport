import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import


def test_dealing_implicit_imports_subpackages():
    # https://github.com/hakancelik96/unimport/issues/127
    source = """\
        import x.y

        x
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []
