from tests.refactor.utils import RefactorTestCase


class AsImportTestCase(RefactorTestCase):
    def test_as_import_all_unused_all_cases(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y as z
            import x
            from t import s as ss
            import le as x
            """
        )

    def test_multiple_from_as_import(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from f import a as c, l as k, i as ii
            from fo import (bar, i, x as z)
            """,
        )

    def test_multiple_import_name_as_import(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            import a as c, l as k, i as ii
            import bar, i, x as z
            """,
        )

    def test_multiple_import_name_as_import_duplicate(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import a as c, l as k, i as ii
            import bar, i, x as z
            import bar, i, x as z
            print(bar)
            """,
            """\
            import bar
            print(bar)
            """,
        )

    def test_as_import_used_all_cases(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y as z
            import x
            from t import s as ss
            import bar, i, x as z
            import le as x
            print(x)
            """,
            """\
            import le as x
            print(x)
            """,
        )
