from tests.analyzer.utils import UnusedTestCase
from unimport.statement import Import, ImportFrom


class DuplicateTestCase(UnusedTestCase):
    def test__all__(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from codeop import compile_command
            import compile_command
            __all__ = ["compile_command"]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="compile_command",
                    package="codeop",
                    star=False,
                ),
            ],
        )

    def test_full_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="y",
                    package="x",
                    star=False,
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    suggestions=[],
                    name="y",
                    package="x",
                    star=False,
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    suggestions=[],
                    name="x",
                    package="t",
                    star=False,
                ),
                Import(lineno=4, column=1, name="re", package="re"),
                Import(lineno=5, column=1, name="ll", package="ll"),
                Import(lineno=6, column=1, name="ll", package="ll"),
                ImportFrom(
                    lineno=7,
                    column=1,
                    suggestions=[],
                    name="e",
                    package="c",
                    star=False,
                ),
                Import(lineno=8, column=1, name="e", package="e"),
            ],
        )

    def test_one_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
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
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="y",
                    package="x",
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
                    lineno=3,
                    column=1,
                    name="x",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=4,
                    column=1,
                    name="re",
                    package="re",
                ),
                Import(
                    lineno=5,
                    column=1,
                    name="ll",
                    package="ll",
                ),
                Import(
                    lineno=6,
                    column=1,
                    name="ll",
                    package="ll",
                ),
                ImportFrom(
                    lineno=7,
                    column=1,
                    name="e",
                    package="c",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=8,
                    column=1,
                    name="e",
                    package="e",
                ),
                ImportFrom(
                    lineno=9,
                    column=1,
                    name="Path",
                    package="pathlib",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_two_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
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
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="y",
                    package="x",
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
                    lineno=3,
                    column=1,
                    name="x",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=4,
                    column=1,
                    name="re",
                    package="re",
                ),
                Import(
                    lineno=5,
                    column=1,
                    name="ll",
                    package="ll",
                ),
                ImportFrom(
                    lineno=7,
                    column=1,
                    name="e",
                    package="c",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=8,
                    column=1,
                    name="e",
                    package="e",
                ),
                ImportFrom(
                    lineno=9,
                    column=1,
                    name="Path",
                    package="pathlib",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_three_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
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
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="y",
                    package="x",
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
                    lineno=3,
                    column=1,
                    name="x",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=4,
                    column=1,
                    name="re",
                    package="re",
                ),
                Import(
                    lineno=5,
                    column=1,
                    name="ll",
                    package="ll",
                ),
                ImportFrom(
                    lineno=7,
                    column=1,
                    name="e",
                    package="c",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=9,
                    column=1,
                    name="Path",
                    package="pathlib",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_different_duplicate_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import z
            from y import z
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="z",
                    package="x",
                    star=False,
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    suggestions=[],
                    name="z",
                    package="y",
                    star=False,
                ),
            ],
        )

    def test_different_duplicate_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import z
            from y import z
            print(z)
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="z",
                    package="x",
                    star=False,
                ),
            ],
        )

    def test_multi_duplicate(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import y, z, t
            import t
            from l import t
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="y",
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
                    column=3,
                    name="t",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=2,
                    column=1,
                    name="t",
                    package="t",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="t",
                    package="l",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_multi_duplicate_one_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import y, z, t
            import t
            from l import t
            print(t)
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="y",
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
                    column=3,
                    name="t",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=2,
                    column=1,
                    name="t",
                    package="t",
                ),
            ],
        )

    def test_one_used_bottom_multi_duplicate(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            print(t)
            """,
            [
                Import(lineno=1, column=1, name="t", package="t"),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="t",
                    package="l",
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
                    lineno=3,
                    column=2,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_two_multi_duplicate_one_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            from i import t, ii
            print(t)
            """,
            [
                Import(
                    lineno=1,
                    column=1,
                    name="t",
                    package="t",
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="t",
                    package="l",
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
                    lineno=3,
                    column=2,
                    name="z",
                    package="x",
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
                    lineno=4,
                    column=2,
                    name="ii",
                    package="i",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_import_in_function(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t

            def function(f=t):
                import x
                return f
            from i import t, ii
            print(t)
            """,
            [
                Import(
                    lineno=1,
                    column=1,
                    name="t",
                    package="t",
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="t",
                    package="l",
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
                    lineno=3,
                    column=2,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=6,
                    column=1,
                    name="x",
                    package="x",
                ),
                ImportFrom(
                    lineno=8,
                    column=2,
                    name="ii",
                    package="i",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_import_in_function_used_two_different(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import t
            print(t)

            from l import t
            from x import y, z, t

            def function(f=t):
                import x
                return f
            from i import t, ii
            print(t)
            """,
            [
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="t",
                    package="l",
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
                    lineno=5,
                    column=2,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=8,
                    column=1,
                    name="x",
                    package="x",
                ),
                ImportFrom(
                    lineno=10,
                    column=2,
                    name="ii",
                    package="i",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_class_scope_import_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import x

            class C:
                import x

                def f(self):
                    x
            """,
            [Import(lineno=4, column=1, name="x", package="x")],
        )

    def test_same_line(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
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
            """,
            [
                Import(
                    lineno=1,
                    column=1,
                    name="x",
                    package="x",
                ),
                Import(
                    lineno=2,
                    column=1,
                    name="e",
                    package="e",
                ),
                Import(
                    lineno=2,
                    column=2,
                    name="y",
                    package="y",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="u",
                    package="z",
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
                    lineno=4,
                    column=2,
                    name="d",
                    package="bb",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=3,
                    name="c",
                    package="bb",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=5,
                    column=1,
                    name="ff",
                    package="ff",
                ),
                Import(
                    lineno=5,
                    column=2,
                    name="tt",
                    package="tt",
                ),
                Import(
                    lineno=5,
                    column=3,
                    name="ff",
                    package="ff",
                ),
                ImportFrom(
                    lineno=6,
                    column=1,
                    name="ll",
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
                    column=5,
                    name="tl",
                    package="ee",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=14,
                    column=1,
                    name="si",
                    package="iss",
                ),
                ImportFrom(
                    lineno=15,
                    column=1,
                    name="ug",
                    package="gu",
                    star=False,
                    suggestions=[],
                ),
            ],
        )
