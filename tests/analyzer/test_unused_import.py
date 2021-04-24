from tests.analyzer.utils import UnusedTestCase
from unimport.statement import Import, ImportFrom


class UnusedImportTestCase(UnusedTestCase):
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
