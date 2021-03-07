import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.constants import PY38_PLUS
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


class SyntaxErrorRefactorTestCase(RefactorTestCase):
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


class UnusedRefactorTestCase(RefactorTestCase):
    def test_do_not_remove_augmented_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from django.conf.global_settings import AUTHENTICATION_BACKENDS, TEMPLATE_CONTEXT_PROCESSORS
            AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)
            """,
            """\
            from django.conf.global_settings import AUTHENTICATION_BACKENDS
            AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)
            """,
        )

    def test_multiple_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x
            import x.y
            import x.y.z
            import x, x.y
            import x, x.y, x.y.z
            import x.y, x.y.z, x.y.z
            import x.y, x.y, x.y.z
            from x import y
            from x import y, z
            from x.y import z, q
            from x.y.z import z, q, zq
            some()
            calls()
            # and comments
            def maybe_functions():
                after()
            from x import (
                y
            )
            from x import (
                y,
                z
            )
            from x import (
                y,
                z,
            )
            from x.y import (
                z,
                q,
                u,
            )
            from x.y import (
                z,
                q,
                u,
                z,
                q,
            )
            """,
            """\
            some()
            calls()
            # and comments
            def maybe_functions():
                after()
            """,
        )

    def test_future_from_import(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from __future__ import (
                absolute_import, division, print_function, unicode_literals
            )
            """
        )

    def test_future_import(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            import __future__
            __future__.absolute_import
            """
        )

    def test_local_import(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from .x import y
            from ..z import t
            from ...t import a
            from .x import y, hakan
            from ..z import u, b
            from ...t import z, q
            hakan
            b
            q()
            """,
            """\
            from .x import hakan
            from ..z import b
            from ...t import q
            hakan
            b
            q()
            """,
        )

    def test_remove_unused_from_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import datetime
            from dateutil.relativedelta import relativedelta
            print(f'The date is {datetime.datetime.now()}.')
            """,
            """\
            import datetime
            print(f'The date is {datetime.datetime.now()}.')
            """,
        )

    def test_inside_function_unused(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            def foo():
                from x import y, z
                try:
                    import t
                    print(t)
                except ImportError as exception:
                    pass
                return math.pi
            """,
            """\
            def foo():
                try:
                    import t
                    print(t)
                except ImportError as exception:
                    pass
                return math.pi
            """,
        )

    def test_comment(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            # This is not unused import, but it is unused import according to unimport.
            # CASE 1
            from codeop import compile_command
            compile_command
            """,
            """\
            # This is not unused import, but it is unused import according to unimport.
            # CASE 1
            from codeop import compile_command
            compile_command
            """,
        )

    def test_star(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from os import *
            walk
            """
        )

    def test_startswith_name(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import xx
            xxx = "test"
            """,
            """\
            xxx = "test"
            """,
        )

    def test_get_star_imp_none(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            try:
                from x import *
            except ImportError:
                pass
            import t
            """,
            """\
            try:
                from x import *
            except ImportError:
                pass
            """,
        )


class DuplicateUnusedRefactorTestCase(RefactorTestCase):
    def test_full_unused(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            """
        )

    def test_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            from pathlib import Path
            from pathlib import Path
            p = Path()
            """,
            """\
            from pathlib import Path
            p = Path()
            """,
        )

    def test_two_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            from pathlib import Path
            from pathlib import Path
            p = Path()
            print(ll)
            """,
            """\
            import ll
            from pathlib import Path
            p = Path()
            print(ll)
            """,
        )

    def test_three_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y
            from x import y
            from t import x
            import re
            import ll
            import ll
            from c import e
            import e
            from pathlib import Path
            from pathlib import Path
            p = Path()
            print(ll)
            def function(e=e):pass
            """,
            """\
            import ll
            import e
            from pathlib import Path
            p = Path()
            print(ll)
            def function(e=e):pass
            """,
        )

    def test_different_duplicate_unused(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import z
            from y import z
            """,
        )

    def test_different_duplicate_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import z
            from y import z
            print(z)
            """,
            """\
            from y import z
            print(z)
            """,
        )

    def test_multi_duplicate(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y, z, t
            import t
            from l import t
            """,
        )

    def test_multi_duplicate_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y, z, t
            import t
            from l import t
            print(t)
            """,
            """\
            from l import t
            print(t)
            """,
        )

    def test_one_used_bottom_multi_duplicate(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            print(t)
            """,
            """\
            from x import t
            print(t)
            """,
        )

    def test_two_multi_duplicate_one_used(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            from i import ii, t
            print(t)
            """,
            """\
            from i import t
            print(t)
            """,
        )

    def test_import_in_function(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            from l import t
            from x import y, z, t
            def function(f=t):
                import x
                return f
            from i import ii, t
            print(t)
            """,
            """\
            from x import t
            def function(f=t):
                return f
            from i import t
            print(t)
            """,
        )

    def test_import_in_function_used_two_different(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import t
            print(t)
            from l import t
            from x import y, z, t
            def function(f=t):
                import x
                return f
            from i import ii, t
            print(t)
            """,
            """\
            import t
            print(t)
            from x import t
            def function(f=t):
                return f
            from i import t
            print(t)
            """,
        )

    def test_startswith_name(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import aa
            aaa
            """,
            """\
            aaa
            """,
        )

    def test_same_line(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x, x, yt
            import e, y, e
            from z import u, u
            from bb import c, d, c, c
            import ff, tt, ff, ff, tt
            from ee import (
               ll,
               el,
               ll,
               el,
               tl,
               tl,
            )
            import iss as si, si
            from gu import ug,\\
            ug

            x, e, u, c, ff, tt, ll, el, tl, si, ug, yt
            """,
            """\
            import x, yt
            import e
            from z import u
            from bb import c
            import ff, tt
            from ee import (
               ll,
               el,
               tl
            )
            import si
            from gu import ug

            x, e, u, c, ff, tt, ll, el, tl, si, ug, yt
            """,
        )


class AsImportTestCase(RefactorTestCase):
    def test_as_import_all_unused_all_cases(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from x import y as z
            import x
            from t import s as ss
            import le as x
            """
        )

    def test_multiple_from_as_import(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            from f import a as c, l as k, i as ii
            from fo import (bar, i, x as z)
            """,
        )

    def test_multiple_import_name_as_import(self):
        self.assertActionAfterRefactorEqualToEmpty(
            """\
            import a as c, l as k, i as ii
            import bar, i, x as z
            """,
        )

    def test_multiple_import_name_as_import_duplicate(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import a as c, l as k, i as ii
            import bar, i, x as z
            import bar, i, x as z
            print(bar)
            """,
            """\
            import bar
            print(bar)
            """,
        )

    def test_as_import_used_all_cases(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import y as z
            import x
            from t import s as ss
            import bar, i, x as z
            import le as x
            print(x)
            """,
            """\
            import le as x
            print(x)
            """,
        )


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


class TypingTestCase(RefactorTestCase):

    include_star_import = True

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comments(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Any
            from typing import Tuple
            from typing import Union
            def function(a, b):
                # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
                pass
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comments_with_variable(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            test_variable = [2] # type: List[int]
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comment_params(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            def x(
               f: # type:List,
               r: # type:str
            ):
               pass
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comment_funcdef(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            def x(y):
               # type: (str) -> List[str]
               pass
            """
        )

    def test_variable(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            test: "List[Dict]"
            """
        )

    def test_function_arg(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            def test(arg:"List[Dict]") -> None:
               pass
            """
        )

    def test_function_str_arg(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, Literal
            def test(item, when: "Literal['Dict']") -> None:
               pas
            """
        )

    def test_function_return(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            def test(arg: list) -> "List[Dict]":
               pass
            """
        )


class TypeVariableTestCase(RefactorTestCase):
    def test_type_assing_union(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebEngineWidgets import QWebEngineHistory
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.Union['QWebEngineHistory', 'QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, Union
                if TYPE_CHECKING:
                   from PyQt5.QtWebEngineWidgets import QWebEngineHistory
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = Union['QWebEngineHistory', 'QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, Union
                if TYPE_CHECKING:
                   from PyQt5 import QtWebEngineWidgets, QtWebKit

                HistoryType = Union['QtWebEngineWidgets.QWebEngineHistory', 'QtWebKit.QWebHistory']

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)

    def test_type_assing_list(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.List['QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, List
                if TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = List['QWebHistory']

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)

    def test_type_assing_cast(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.cast('QWebHistory', None)

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING
                if TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = cast('QWebHistory', return_value)

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING
                if TYPE_CHECKING:
                   from PyQt5 import QtWebKit

                HistoryType = cast('QtWebKit.QWebHistory', return_value)

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)


class StyleTestCase(RefactorTestCase):
    def test_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            import u
            y, q, e, r, t
            """,
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            y, q, e, r, t
            """,
        )

    def test_2_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t
            )
            import y
            import u
            y, q, e, t
            """,
            """\
            from x import (
               q,
               e,
               t
            )
            import y
            y, q, e, t
            """,
        )

    def test_3_1_vertical(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (
               q,
               e,
               r,
               t,
            )
            import y
            import u
            y, q, e, r
            """,
            """\
            from x import (
               q,
               e,
               r
            )
            import y
            y, q, e, r
            """,
        )

    def test_4_1_paren_horizontal(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from x import (q, e, r, t)
            import y
            import u
            y, q, e, r
            """,
            """\
            from x import (q, e, r)
            import y
            y, q, e, r
            """,
        )
