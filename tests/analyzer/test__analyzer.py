import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.statement import Import


class AnalyzerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        Analyzer.clear()

    def test_context_manager(self):
        with Analyzer(
            source=textwrap.dedent(
                """\
                import x
                """
            )
        ):
            self.assertEqual(1, len(Import.imports))

        self.assertEqual(0, len(Import.imports))
