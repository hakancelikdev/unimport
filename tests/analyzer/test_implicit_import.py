from tests.analyzer.utils import UnusedTestCase


class DealingImplicitImportsSubPackagesTestCase(UnusedTestCase):
    # https://github.com/hakancelik96/unimport/issues/127

    def test(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            import x.y

            x
            """,
        )
