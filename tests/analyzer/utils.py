import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.statement import Import, Name


class AnalyzerTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self) -> None:
        Analyzer.clear()

    def assertUnimportEqual(
        self,
        source,
        expected_names=[],
        expected_imports=[],
    ):
        analyzer = Analyzer(
            source=textwrap.dedent(source),
            include_star_import=self.include_star_import,
        )
        analyzer.traverse()
        self.assertListEqual(expected_names, Name.names)
        self.assertListEqual(expected_imports, Import.imports)


class UnusedTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self) -> None:
        Analyzer.clear()

    def assertSourceAfterScanningEqualToExpected(
        self, source, expected_unused_imports=[]
    ):
        analyzer = Analyzer(
            source=textwrap.dedent(source),
            include_star_import=self.include_star_import,
        )
        analyzer.traverse()
        self.assertListEqual(
            list(reversed(expected_unused_imports)),
            list(Import.get_unused_imports(self.include_star_import)),
        )
