import textwrap
import unittest

from tests.analyzer.utils import AnalyzerTestCase
from unimport.analyzer import Analyzer
from unimport.constants import PY38_PLUS
from unimport.statement import Import, ImportFrom, Name


class SkipImportTestCase(AnalyzerTestCase):
    def test_inside_try_except(self):
        self.assertUnimportEqual(
            source="""\
            try:
               import django
            except ImportError:
               print('install django')
            """,
            expected_names=[
                Name(lineno=3, name="ImportError"),
                Name(lineno=4, name="print"),
            ],
        )

    def test_as_import(self):
        self.assertUnimportEqual(source="from x import y as z # unimport:skip")

    def test_ongoing_comment(self):
        self.assertUnimportEqual(
            source="import unimport # unimport:skip import test"
        )

    def test_skip_comment_second_option(self):
        self.assertUnimportEqual(source="import x # unimport:skip test")

    def test_noqa_skip_comment(self):
        self.assertUnimportEqual(source="from x import (t, y, f, r) # noqa")

    def test_noqa_skip_comment_multiple(self):
        self.assertUnimportEqual(
            source="""\
            from x import ( # noqa
               t, y,
               f, r
            )
            """
        )

    def test_skip_file(self):
        self.assertUnimportEqual(
            source="""\
            # unimport:skip_file
            import x"
            """
        )

    def test_skip_file_after_import(self):
        self.assertUnimportEqual(
            source="""\
            import x
            # unimport:skip_file
            """
        )

    def test_skip_comment_after_any_comment(self):
        self.assertUnimportEqual(
            source="import x # any test comment unimport:skip any test comment"
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_skip_comment_multiline(self):
        self.assertUnimportEqual(
            source="""\
            from package import (
                module
            ) # unimport: skip
            """
        )
        self.assertUnimportEqual(
            source="""\
            import x
            import y
            from package import (
                module,
                module,
                module,
            )  # unimport: skip
            """,
            expected_imports=[
                Import(lineno=1, column=1, name="x", package="x"),
                Import(lineno=2, column=1, name="y", package="y"),
            ],
        )

    def test_space_between(self):
        """https://github.com/hakancelik96/unimport/issues/146."""
        self.assertUnimportEqual(
            source="""\
            import math

            import collections  # noqa
            """,
            expected_imports=[
                Import(lineno=1, column=1, name="math", package="math"),
            ],
        )
