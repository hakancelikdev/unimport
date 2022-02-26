import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, ImportFrom, Name


def test_call_in_name():
    source = """\
        from pathlib import Path
        CURRENT_DIR = Path(__file__).parent
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
        ]
        assert Name.names == [
            Name(lineno=2, name="CURRENT_DIR"),
            Name(lineno=2, name="Path"),
            Name(lineno=2, name="__file__"),
        ]


def test_call_in_attr():
    source = """\
        a(b.c).d
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=1, name="a"),
            Name(lineno=1, name="b.c"),
        ]


def test_call_in_str_attr():
    source = """\
        a("b.c").d
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=1, name="a"),
        ]


def test_attr_in_call_in_attr():
    source = """\
        a.b(c.d).f
        """
    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=1, name="a.b"),
            Name(lineno=1, name="c.d"),
        ]
