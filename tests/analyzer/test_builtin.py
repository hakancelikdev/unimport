import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import


def test_ConnectionError():
    # https://github.com/hakancelik96/unimport/issues/45
    source = """\
        from x.y import ConnectionError
        try:
           pass
        except ConnectionError:
           pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []


def test_ValueError():
    # https://github.com/hakancelik96/unimport/issues/45
    source = """\
        from x import ValueError
        print(ValueError)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []


def test_builtins():
    # https://github.com/hakancelik96/unimport/issues/45
    source = """\
        from builtins import next, object, range
        __all__ = ["next", "object"]
        for i in range(8):
           pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []
