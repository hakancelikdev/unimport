import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, ImportFrom


def test__all__():
    source = """\
        from codeop import compile_command
        import compile_command
        __all__ = ["compile_command"]
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="compile_command",
                package="codeop",
                star=False,
            ),
        ]


def test_full_unused():
    source = """\
        from x import y
        from x import y
        from t import x
        import re
        import ll
        import ll
        from c import e
        import e
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            Import(lineno=8, column=1, name="e", package="e"),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(lineno=6, column=1, name="ll", package="ll"),
            Import(lineno=5, column=1, name="ll", package="ll"),
            Import(lineno=4, column=1, name="re", package="re"),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_one_used():
    source = """\
        from x import y
        from x import y
        from t import x
        import re
        import ll
        import ll
        from c import e
        import e
        from pathlib import Path
        from pathlib import Path
        p = Path()
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
            Import(lineno=8, column=1, name="e", package="e"),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(lineno=6, column=1, name="ll", package="ll"),
            Import(lineno=5, column=1, name="ll", package="ll"),
            Import(lineno=4, column=1, name="re", package="re"),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_two_used():
    source = """\
        from x import y
        from x import y
        from t import x
        import re
        import ll
        import ll
        from c import e
        import e
        from pathlib import Path
        from pathlib import Path
        p = Path()
        print(ll)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
            Import(lineno=8, column=1, name="e", package="e"),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(lineno=5, column=1, name="ll", package="ll"),
            Import(lineno=4, column=1, name="re", package="re"),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_three_used():
    source = """\
        from x import y
        from x import y
        from t import x
        import re
        import ll
        import ll
        from c import e
        import e
        from pathlib import Path
        from pathlib import Path
        p = Path()
        print(ll)
        def function(e=e):pass
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(lineno=5, column=1, name="ll", package="ll"),
            Import(lineno=4, column=1, name="re", package="re"),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_different_duplicate_unused():
    source = """\
        from x import z
        from y import z
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=2,
                column=1,
                suggestions=[],
                name="z",
                package="y",
                star=False,
            ),
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="z",
                package="x",
                star=False,
            ),
        ]


def test_different_duplicate_used():
    source = """\
        from x import z
        from y import z
        print(z)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="z",
                package="x",
                star=False,
            ),
        ]


def test_multi_duplicate():
    source = """\
        from x import y, z, t
        import t
        from l import t
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=3,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            Import(lineno=2, column=1, name="t", package="t"),
            ImportFrom(
                lineno=1,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_multi_duplicate_one_used():
    source = """\
        from x import y, z, t
        import t
        from l import t
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            Import(lineno=2, column=1, name="t", package="t"),
            ImportFrom(
                lineno=1,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]


def test_one_used_bottom_multi_duplicate():
    source = """\
        import t
        from l import t
        from x import y, z, t
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            Import(lineno=1, column=1, name="t", package="t"),
        ]


def test_two_multi_duplicate_one_used():
    source = """\
        import t
        from l import t
        from x import y, z, t
        from i import t, ii
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=4,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            Import(lineno=1, column=1, name="t", package="t"),
        ]


def test_import_in_function():
    source = """\
        import t
        from l import t
        from x import y, z, t

        def function(f=t):
            import x
            return f
        from i import t, ii
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=8,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
            Import(lineno=6, column=1, name="x", package="x"),
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            Import(lineno=1, column=1, name="t", package="t"),
        ]


def test_import_in_function_used_two_different():
    source = """\
        import t
        print(t)

        from l import t
        from x import y, z, t

        def function(f=t):
            import x
            return f
        from i import t, ii
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=10,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
            Import(lineno=8, column=1, name="x", package="x"),
            ImportFrom(
                lineno=5,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
        ]


# def test_class_scope_import_unused():
# NOTE; Support, will be given later.
#     self.assertSourceAfterScanningEqualToExpected(
#         """\
#         import x

#         class C:
#             import x

#             def f():
#                 x
#         """,
#         [Import(lineno=4, column=1, name="x", package="x")],
#     )

#     self.assertSourceAfterScanningEqualToExpected(
#         """\
#         import x

#         class C:
#             def f():
#                 import x

#                 def f():
#                     x
#         """,
#         [
#             Import(lineno=4, column=1, name='x', package='x'),
#             Import(lineno=1, column=1, name='x', package='x'),
#         ],
#     )


def test_same_line():
    source = """\
        import x, x, yt
        import e, y, e
        from z import u, u
        from bb import c, d, c, c
        import ff, tt, ff, ff, tt
        from ee import (
           ll,
           el,
           ll,
           el,
           tl,
           tl,
        )
        import iss as si, si
        from gu import ug,\
        ug

        x, e, u, c, ff, tt, ll, el, tl, si, ug, yt
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=15,
                column=1,
                name="ug",
                package="gu",
                star=False,
                suggestions=[],
            ),
            Import(lineno=14, column=1, name="si", package="iss"),
            ImportFrom(
                lineno=6,
                column=5,
                name="tl",
                package="ee",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=6,
                column=2,
                name="el",
                package="ee",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=6,
                column=1,
                name="ll",
                package="ee",
                star=False,
                suggestions=[],
            ),
            Import(lineno=5, column=3, name="ff", package="ff"),
            Import(lineno=5, column=2, name="tt", package="tt"),
            Import(lineno=5, column=1, name="ff", package="ff"),
            ImportFrom(
                lineno=4,
                column=3,
                name="c",
                package="bb",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=2,
                name="d",
                package="bb",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="c",
                package="bb",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="u",
                package="z",
                star=False,
                suggestions=[],
            ),
            Import(lineno=2, column=2, name="y", package="y"),
            Import(lineno=2, column=1, name="e", package="e"),
            Import(lineno=1, column=1, name="x", package="x"),
        ]


def test_function_scope_same():
    source = """\
        def c():
            import x

            x.s


        def d():
            import x

            x.s
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []
