import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.refactor import refactor_string


class RefactorTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def refactor(self, action: str) -> str:
        analyzer = Analyzer(
            source=textwrap.dedent(action),
            include_star_import=self.include_star_import,
        )
        analyzer.traverse()
        refactor_result = refactor_string(
            source=analyzer.source,
            unused_imports=list(analyzer.get_unused_imports()),
        )
        return refactor_result

    def assertActionAfterRefactorEqualToAction(self, action):
        super().assertEqual(textwrap.dedent(action), self.refactor(action))

    def assertActionAfterRefactorEqualToExpected(self, action, expected):
        super().assertEqual(textwrap.dedent(expected), self.refactor(action))

    def assertActionAfterRefactorEqualToEmpty(self, action):
        self.assertActionAfterRefactorEqualToExpected(
            action,
            """\

            """,
        )
