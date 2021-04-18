from tests.analyzer.utils import UnusedTestCase


class AllTestCase(UnusedTestCase):
    def test_from_import(self):
        self.assertSourceAfterScanningEqualToExpected(
            """\
            from codeop import compile_command
            __all__ = ["compile_command"]
            """
        )

    def test_defined_top(self):
        self.assertSourceAfterScanningEqualToExpected(
            source="""\
            __all__ = ["x"]
            import x
            """,
        )
