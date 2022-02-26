import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, ImportFrom, Name


def test_star():
    source = """\
        from os import *
        __all__ = ["walk", "removedirs"]
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="__all__"),
            Name(lineno=2, name="walk", is_all=True),
            Name(lineno=2, name="removedirs", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=["removedirs", "walk"],
            )
        ]


def test_append():
    source = """\
        from os import *
        __all__ = ["walk"]
        __all__.append("removedirs")
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="__all__"),
            Name(lineno=3, name="__all__.append"),
            Name(lineno=2, name="walk", is_all=True),
            Name(lineno=3, name="removedirs", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=["removedirs", "walk"],
            )
        ]


def test_extend():
    source = """\
        from os import *
        __all__ = ["walk"]
        __all__.extend(["removedirs"])
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="__all__"),
            Name(lineno=3, name="__all__.extend"),
            Name(lineno=2, name="walk", is_all=True),
            Name(lineno=3, name="removedirs", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=["removedirs", "walk"],
            )
        ]


def test_star_unused():
    source = """\
        from os import *
        __all__ = ["test"]
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="__all__"),
            Name(lineno=2, name="test", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=[],
            )
        ]


def test_unknown():
    source = """\
        from x import *
        __all__ = ["xx"]
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="__all__"),
            Name(lineno=2, name="xx", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="x",
                package="x",
                star=True,
                suggestions=[],
            )
        ]


def test_unused():
    source = """\
        from os import *
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=[],
            )
        ]


def test_used():
    source = """\
        from os import *
        print(walk)
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=2, name="print"),
            Name(lineno=2, name="walk"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=["walk"],
            )
        ]


def test_used_and_unused():
    source = """\
        from lib2to3.fixer_util import *
        from lib2to3.pytree import *
        from lib2to3.pgen2 import token
        BlankLine, FromImport, Leaf, Newline, Node
        token.NAME, token.STAR
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=4, name="BlankLine"),
            Name(lineno=4, name="FromImport"),
            Name(lineno=4, name="Leaf"),
            Name(lineno=4, name="Newline"),
            Name(lineno=4, name="Node"),
            Name(lineno=5, name="token.NAME"),
            Name(lineno=5, name="token.STAR"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="lib2to3.fixer_util",
                package="lib2to3.fixer_util",
                star=True,
                suggestions=[
                    "BlankLine",
                    "FromImport",
                    "Leaf",
                    "Newline",
                    "Node",
                    "token",
                ],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="lib2to3.pytree",
                package="lib2to3.pytree",
                star=True,
                suggestions=["Leaf", "Node"],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="token",
                package="lib2to3.pgen2",
                star=False,
                suggestions=[],
            ),
        ]


def test_used_and_unused_2():
    source = """\
        from lib2to3.fixer_util import *
        from lib2to3.pytree import *
        from lib2to3.pgen2.token import *
        BlankLine, FromImport, Leaf, Newline, Node
        NAME, STAR
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=4, name="BlankLine"),
            Name(lineno=4, name="FromImport"),
            Name(lineno=4, name="Leaf"),
            Name(lineno=4, name="Newline"),
            Name(lineno=4, name="Node"),
            Name(lineno=5, name="NAME"),
            Name(lineno=5, name="STAR"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="lib2to3.fixer_util",
                package="lib2to3.fixer_util",
                star=True,
                suggestions=[
                    "BlankLine",
                    "FromImport",
                    "Leaf",
                    "Newline",
                    "Node",
                ],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="lib2to3.pytree",
                package="lib2to3.pytree",
                star=True,
                suggestions=["Leaf", "Node"],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="lib2to3.pgen2.token",
                package="lib2to3.pgen2.token",
                star=True,
                suggestions=["NAME", "STAR"],
            ),
        ]


def test_defined_all():
    source = """\
        from ast import *

        __all__ = []
        __all__.append("x")
        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=3, name="__all__"),
            Name(lineno=4, name="__all__.append"),
            Name(lineno=4, name="x", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="ast",
                package="ast",
                star=True,
                suggestions=[],
            )
        ]


def test_defined_class():
    source = """\
        __all__ = ["NodeVisitor", "parse"]

        from ast import *

        class NodeVisitor:
            ...

        literal_eval

        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=1, name="__all__"),
            Name(lineno=8, name="literal_eval"),
            Name(lineno=1, name="NodeVisitor", is_all=True),
            Name(lineno=1, name="parse", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=3,
                column=1,
                name="ast",
                package="ast",
                star=True,
                suggestions=["literal_eval", "parse"],
            )
        ]


def test_defined_function():
    source = """\
        from ast import *

        __all__.extend(["NodeVisitor", "parse"])

        def literal_eval():
            ...

        """

    with Analyzer(source=textwrap.dedent(source), include_star_import=True):
        assert Name.names == [
            Name(lineno=3, name="__all__.extend"),
            Name(lineno=3, name="NodeVisitor", is_all=True),
            Name(lineno=3, name="parse", is_all=True),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="ast",
                package="ast",
                star=True,
                suggestions=["NodeVisitor", "parse"],
            )
        ]
