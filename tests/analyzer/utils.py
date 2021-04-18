import textwrap
import unittest

from unimport.analyzer import Analyzer


class AnalyzerTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

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
        self.assertEqual(expected_names, analyzer.names)
        self.assertEqual(expected_imports, analyzer.imports)
        analyzer.clear()


class UnusedTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def assertSourceAfterScanningEqualToExpected(
        self, source, expected_unused_imports=[]
    ):
        analyzer = Analyzer(
            source=textwrap.dedent(source),
            include_star_import=self.include_star_import,
        )
        analyzer.traverse()
        super().assertEqual(
            expected_unused_imports,
            list(analyzer.get_unused_imports()),
        )
        analyzer.clear()
