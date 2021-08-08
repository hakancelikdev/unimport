import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.refactor import refactor_string
from unimport.statement import Import


class RefactorTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self) -> None:
        Analyzer.clear()

    def refactor(self, action: str) -> str:
        analyzer = Analyzer(
            source=textwrap.dedent(action),
            include_star_import=self.include_star_import,
        )
        analyzer.traverse()
        refactor_result = refactor_string(
            source=analyzer.source,
            unused_imports=list(
                Import.get_unused_imports(self.include_star_import)
            ),
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
