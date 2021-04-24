import unittest

from tests.refactor.utils import RefactorTestCase


@unittest.skip("Temporarily removed.")
class DuplicateImportTestCase(RefactorTestCase):
    def test_full_unused(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            """
        )

    def test_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
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
            """\
            from pathlib import Path
            p = Path()
            """,
        )

    def test_two_used(self):
        self.assertActionAfterRefactorEqualToExpected(
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
            """\
            import ll
            from pathlib import Path
            p = Path()
            print(ll)
            """,
        )

    def test_three_used(self):
        self.assertActionAfterRefactorEqualToExpected(
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
            """\
            import ll
            import e
            from pathlib import Path
            p = Path()
            print(ll)
            def function(e=e):pass
            """,
        )

    def test_different_duplicate_unused(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import z
            from y import z
            """,
        )

    def test_different_duplicate_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import z
            from y import z
            print(z)
            """,
            """\
            from y import z
            print(z)
            """,
        )

    def test_multi_duplicate(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y, z, t
            import t
            from l import t
            """,
        )

    def test_multi_duplicate_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y, z, t
            import t
            from l import t
            print(t)
            """,
            """\
            from l import t
            print(t)
            """,
        )

    def test_one_used_bottom_multi_duplicate(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            print(t)
            """,
            """\
            from x import t
            print(t)
            """,
        )

    def test_two_multi_duplicate_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            from i import ii, t
            print(t)
            """,
            """\
            from i import t
            print(t)
            """,
        )

    def test_import_in_function(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            def function(f=t):
                import x
                return f
            from i import ii, t
            print(t)
            """,
            """\
            from x import t
            def function(f=t):
                return f
            from i import t
            print(t)
            """,
        )

    def test_import_in_function_used_two_different(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            print(t)
            from l import t
            from x import y, z, t
            def function(f=t):
                import x
                return f
            from i import ii, t
            print(t)
            """,
            """\
            import t
            print(t)
            from x import t
            def function(f=t):
                return f
            from i import t
            print(t)
            """,
        )

    def test_startswith_name(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import aa
            aaa
            """,
            """\
            aaa
            """,
        )

    def test_same_line(self):
        self.assertActionAfterRefactorEqualToExpected(
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
            from gu import ug,\\
            ug

            x, e, u, c, ff, tt, ll, el, tl, si, ug, yt
            """,
            """\
            import x, yt
            import e
            from z import u
            from bb import c
            import ff, tt
            from ee import (
               ll,
               el,
               tl
            )
            import si
            from gu import ug

            x, e, u, c, ff, tt, ll, el, tl, si, ug, yt
            """,
        )
