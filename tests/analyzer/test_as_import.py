from tests.analyzer.utils import UnusedTestCase
from unimport.statement import Import, ImportFrom


class AsImportTestCase(UnusedTestCase):
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
