from tests.analyzer.utils import UnusedTestCase


class BuiltinTestCase(UnusedTestCase):
    # https://github.com/hakancelik96/unimport/issues/45

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
