import textwrap
import unittest

from unimport.scan import Scanner
from unimport.statement import Import, ImportFrom


class UnusedTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def assertSourceAfterScanningEqualToExpected(
        self, source, expected_unused_imports=[]
    ):
        scanner = Scanner(
            source=textwrap.dedent(source),
            include_star_import=self.include_star_import,
        )
        scanner.traverse()
        super().assertEqual(
            list(scanner.get_unused_imports()),
            expected_unused_imports,
        )
        scanner.clear()


class TestBuiltin(UnusedTestCase):
    include_star_import = True

    def test_ConnectionError(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x.y import ConnectionError
            try:
               pass
            except ConnectionError:
               pass
            """
        )

    def test_ValueError(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import ValueError
            print(ValueError)
            """
        )

    def test_builtins(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from builtins import next, object, range
            __all__ = ["next", "object"]
            for i in range(8):
               pass
            """
        )


class Test__All__(UnusedTestCase):
    include_star_import = True

    def test_from_import(self):
        # in this case this import is used
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from codeop import compile_command
            __all__ = ["compile_command"]
            """
        )

    def test_star(self):
        # in this case this import is used
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = ["walk", "removedirs"]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=["removedirs", "walk"],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_append(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = ["walk"]
            __all__.append("removedirs")
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=["removedirs", "walk"],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_extend(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = ["walk"]
            __all__.extend(["removedirs"])
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=["removedirs", "walk"],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_star_unused(self):
        # in this case this import is unused
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = ["test"]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_plus_bin_op(self):
        # NOTE no support.
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = ["w" + "alk"]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_list_comprehension(self):
        # NOTE no support.
        source = ()
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            __all__ = [expression for item in ["os", "walk"]]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="os",
                    package="os",
                    star=True,
                ),
            ],
        )

    def test_unknown(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import *
            __all__ = ["xx"]
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="x",
                    package="x",
                    star=True,
                ),
            ],
        )


class TestUnusedImport(UnusedTestCase):
    include_star_import = True

    def test_comma(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import (
                waitpid,
                scandir,
            )
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="waitpid",
                    package="os",
                    star=False,
                ),
                ImportFrom(
                    lineno=1,
                    column=2,
                    suggestions=[],
                    name="scandir",
                    package="os",
                    star=False,
                ),
            ],
        )

    def test_module_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from pathlib import Path
            CURRENT_DIR = Path(".").parent
            """
        )

    def test_module_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from pathlib import Path
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    suggestions=[],
                    name="Path",
                    package="pathlib",
                    star=False,
                ),
            ],
        )

    def test_unknown_module_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import x.y
            CURRENT_DIR = x.y(".").parent
            """
        )

    def test_unknown_module_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import x.y
            import d.f.a.s
            CURRENT_DIR = x.y(".").parent
            """,
            [
                Import(
                    lineno=2,
                    column=1,
                    name="d.f.a.s",
                    package="d.f.a.s",
                ),
            ],
        )

    def test_import_in_function(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import t
            from x import y, z

            def function(f=t):
                import x
                return f
            from i import t, ii
            print(t)
            """,
            [
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="y",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=2,
                    column=2,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=5,
                    column=1,
                    name="x",
                    package="x",
                ),
                ImportFrom(
                    lineno=7,
                    column=2,
                    name="ii",
                    package="i",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_import_after_usage(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            def function():
                print(os)
                import os
            """,
            [Import(lineno=3, column=1, name="os", package="os")],
        )

    def test_double_underscore_builtins_names(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from globals import (
                __name__, __doc__, __package__,
               __loader__, __spec__, __annotations__,
               __builtins__
            )
            __name__, __doc__, __package__,
            __loader__, __spec__, __annotations__,
            __builtins__
            """
        )


class TestStarImport(UnusedTestCase):
    include_star_import = True

    def test_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=[],
                ),
            ],
        )

    def test_used(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from os import *
            print(walk)
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["walk"],
                ),
            ],
        )

    def test_used_and_unused(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from lib2to3.fixer_util import *
            from lib2to3.pytree import *
            from lib2to3.pgen2 import token
            BlankLine, FromImport, Leaf, Newline, Node
            token.NAME, token.STAR
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="lib2to3.fixer_util",
                    package="lib2to3.fixer_util",
                    star=True,
                    suggestions=[
                        "BlankLine",
                        "FromImport",
                        "Leaf",  #
                        "Newline",
                        "Node",  #
                        "token",  #
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
            ],
        )

    def test_used_and_unused_2(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from lib2to3.fixer_util import *
            from lib2to3.pytree import *
            from lib2to3.pgen2.token import *
            BlankLine, FromImport, Leaf, Newline, Node
            NAME, STAR
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="lib2to3.fixer_util",
                    package="lib2to3.fixer_util",
                    star=True,
                    suggestions=[
                        "BlankLine",
                        "FromImport",
                        "Leaf",  #
                        "Newline",
                        "Node",  #
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
            ],
        )


class TestDuplicate(UnusedTestCase):
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


class TestAsImport(UnusedTestCase):
    def test_as_import_all_unused_all_cases(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import y as z
            import x
            from t import s as ss
            from f import a as c, l as k, i as ii
            from fo import (bar, i, x as z)
            import le as x
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=2,
                    column=1,
                    name="x",
                    package="x",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="ss",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="c",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=2,
                    name="k",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=3,
                    name="ii",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=1,
                    name="bar",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=2,
                    name="i",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=3,
                    name="z",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=6,
                    column=1,
                    name="x",
                    package="le",
                ),
            ],
        )

    def test_as_import_one_used_in_function_all_cases(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from x import y as z
            import x
            from t import s as ss
            from f import a as c, l as k, i as ii
            from fo import (bar, i, x as z)
            import le as x
            def x(t=x):pass
            """,
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                ),
                Import(
                    lineno=2,
                    column=1,
                    name="x",
                    package="x",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="ss",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="c",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=2,
                    name="k",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=3,
                    name="ii",
                    package="f",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=1,
                    name="bar",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=2,
                    name="i",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=5,
                    column=3,
                    name="z",
                    package="fo",
                    star=False,
                    suggestions=[],
                ),
            ],
        )
