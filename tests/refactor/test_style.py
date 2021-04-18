from tests.refactor.utils import RefactorTestCase


class StyleTestCase(RefactorTestCase):
    def test_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            import u
            y, q, e, r, t
            """,
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            y, q, e, r, t
            """,
        )

    def test_2_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            import u
            y, q, e, t
            """,
            """\
            from x import (
               q,
               e,
               t
            )
            import y
            y, q, e, t
            """,
        )

    def test_3_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t,
            )
            import y
            import u
            y, q, e, r
            """,
            """\
            from x import (
               q,
               e,
               r
            )
            import y
            y, q, e, r
            """,
        )

    def test_4_1_paren_horizontal(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (q, e, r, t)
            import y
            import u
            y, q, e, r
            """,
            """\
            from x import (q, e, r)
            import y
            y, q, e, r
            """,
        )
