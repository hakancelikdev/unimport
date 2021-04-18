import unittest

from tests.refactor.utils import RefactorTestCase
from unimport.constants import PY38_PLUS


class SyntaxErrorTestCase(RefactorTestCase):
    def test_syntax_error(self):
        self.assertActionAfterRefactorEqualToAction("a :? = 0")

    def test_bad_syntax(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            # -*- coding: utf-8 -*-
            € = 2
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comments(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            def function(): # type: blabla
                pass
            """
        )


class ImportErrorTestCase(RefactorTestCase):
    """Unimport skip imports controlled by ImportError."""

    include_star_import = True

    def test_import_else_another(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            try:
               import x
            except ImportError:
                import y as x
            print(x)
            """
        )

    def test_as_import(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            try:
                import x
            except ImportError as err:
                print('try this code `pip install x`')
            """
        )

    def test_tuple(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            try:
                import xa
            except (A, ImportError):
                pass
            """
        )

    def test_inside_function_unused(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            def foo():
                from abc import *
                try:
                    import t
                    print(ABCMeta)
                except ImportError as exception:
                    pass
                return math.pi
            """,
            """\
            def foo():
                from abc import ABCMeta
                try:
                    import t
                    print(ABCMeta)
                except ImportError as exception:
                    pass
                return math.pi
            """,
        )
