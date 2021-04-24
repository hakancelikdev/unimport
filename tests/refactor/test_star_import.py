from tests.refactor.utils import RefactorTestCase


class StarImportTestCase(RefactorTestCase):
    include_star_import = True

    def test_star_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from os import *
            from x import y
            from re import *
            from t.s.d import *
            from lib2to3.pgen2.token import *
            from lib2to3.fixer_util import *
            print(match)
            print(search)
            print(NAME)
            """,
            """\
            from re import match, search
            from lib2to3.pgen2.token import NAME
            print(match)
            print(search)
            print(NAME)
            """,
        )

    def test_star_import_2(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from typing import (
                Callable,
                Iterable,
                Iterator,
                List,
                Optional,
                Text,
                Tuple,
                Pattern,
                Union,
                cast,
            )
            from lib2to3.pgen2.token import *
            from lib2to3.pgen2.grammar import *
            print(Grammar)
            """,
            """\
            from lib2to3.pgen2.grammar import Grammar
            print(Grammar)
            """,
        )

    def test_two_suggestions(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from time import *
            from os import *
            time()  # Function from time module.
            path.join()
            """,
            """\
            from time import time
            from os import path
            time()  # Function from time module.
            path.join()
            """,
        )

    def test_get_source_from_importable_names(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from libcst.metadata import *
            CodeRange, PositionProvider
            """,
            """\
            from libcst.metadata import CodeRange, PositionProvider
            CodeRange, PositionProvider
            """,
        )
