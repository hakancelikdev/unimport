import textwrap
import unittest

from unimport.constants import PY38_PLUS
from unimport.scan import ImportableVisitor, Scanner
from unimport.statement import Import, ImportFrom, Name


class ScannerTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def assertUnimportEqual(
        self,
        source,
        expected_names=[],
        expected_imports=[],
    ):
        scanner = Scanner(
            source=textwrap.dedent(source),
            include_star_import=self.include_star_import,
        )
        self.assertEqual(expected_names, scanner.names)
        if self.include_star_import:
            self.assertEqual(
                expected_imports, list(scanner.get_unused_imports())
            )
        else:
            self.assertEqual(expected_imports, scanner.imports)
        scanner.clear()


class TestNames(ScannerTestCase):
    def test_names(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            variable1 = 2
            class TestClass:
               pass
            def function():
               pass
            """,
        )

    def test_names_with_import(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            import os
            class TestClass():
               def test_function(self):
                   pass
            def test_function():
               pass
            """,
            expected_imports=[
                Import(lineno=2, column=1, name="os", package="os")
            ],
        )

    def test_names_with_function(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            def test():
               pass
            """,
        )

    def test_names_with_class(self):
        self.assertUnimportEqual(
            source="""\
            variable = 1
            def test_function():
               pass
            class test():
               def test_function():
                   pass
            """,
        )

    def test_decator_in_class(self):
        self.assertUnimportEqual(
            source="""\
            class Test:
                def test(self):
                    def test2():
                        return 'test2'
                    return test2
            """,
            expected_names=[Name(lineno=5, name="test2")],
        )


class TestStarImport(ScannerTestCase):
    include_star_import = True

    def test_all_assing_after_attribute_usage(self):
        self.assertUnimportEqual(
            source="""\
            from os import *

            __all__ = []
            __all__.append("walk")
            """,
            expected_names=[Name(lineno=4, name="walk")],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["walk"],
                )
            ],
        )

    def test_assing_after_attribute_usage(self):
        self.assertUnimportEqual(
            source="""\
            from ast import *

            NodeVisitor.s = 0
            NodeVisitor()
            """,
            expected_names=[
                Name(lineno=3, name="NodeVisitor.s"),
                Name(lineno=4, name="NodeVisitor"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="ast",
                    package="ast",
                    star=True,
                    suggestions=["NodeVisitor"],
                )
            ],
        )


class TestAssing(ScannerTestCase):
    include_star_import = True

    def test_star_import_attribute(self):
        self.assertUnimportEqual(
            source="""\
            from os import *

            walk.a = 0
            """,
            expected_names=[Name(lineno=3, name="walk.a")],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["walk"],
                )
            ],
        )

    def test_star_import_name(self):
        self.assertUnimportEqual(
            source="""\
            from os import *

            __all__ = []
            """,
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=[],
                )
            ],
        )

    def test_i120(self):
        # https://github.com/hakancelik96/unimport/issues/120

        self.assertUnimportEqual(
            source="""\
            import datetime
            datetime = None
            import datetime
            """,
            expected_imports=[
                Import(
                    lineno=1, column=1, name="datetime", package="datetime"
                ),
                Import(
                    lineno=3, column=1, name="datetime", package="datetime"
                ),
            ],
        )

    def test_assing_after_import_again(self):

        self.assertUnimportEqual(
            source="""\
            import datetime
            datetime = None
            import datetime
            datetime
            """,
            expected_names=[Name(lineno=4, name="datetime")],
            expected_imports=[
                Import(
                    lineno=1, column=1, name="datetime", package="datetime"
                ),
            ],
        )

    def test_assing_after_import_again_used(self):

        self.assertUnimportEqual(
            source="""\
            import datetime
            x = datetime
            """,
            expected_names=[Name(lineno=2, name="datetime")],
        )


class SkipImportTest(ScannerTestCase):
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


@unittest.skipIf(
    not PY38_PLUS, "This feature is only available for python 3.8."
)
class TestTypeComments(ScannerTestCase):
    def test_type_comments(self):
        self.assertUnimportEqual(
            source="""\
            from typing import Any
            from typing import Tuple
            from typing import Union
            def function(a, b):
                # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
                pass
            """,
            expected_names=[
                Name(lineno=4, name="Any"),
                Name(lineno=4, name="str"),
                Name(lineno=4, name="Union"),
                Name(lineno=4, name="Tuple"),
                Name(lineno=4, name="Tuple"),
                Name(lineno=4, name="str"),
                Name(lineno=4, name="str"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="Any",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="Tuple",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="Union",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
            ],
        )


class TestImportable(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.importable = ImportableVisitor()

    def test_get_names_from_all(self):
        self.importable.traverse(
            textwrap.dedent(
                """\
                __all__ = ["test"]
                __all__.append("test2")
                __all__.extend(["test3"])
                """
            )
        )
        expected = frozenset({"test3", "test", "test2"})
        self.assertEqual(expected, self.importable.get_all())

    def test_get_names_from_suggestion(self):

        self.importable.traverse(
            textwrap.dedent(
                """\
                import xx
                class A:
                   pass
                def b():
                   FUNCNAME = "test"
                NAME="NAME"
                """
            )
        )
        expected = frozenset({"xx", "A", "b", "FUNCNAME", "NAME"})
        self.assertEqual(expected, self.importable.get_suggestion())


class TestTypeVariable(ScannerTestCase):
    def test_union_import(self):
        self.assertUnimportEqual(
            source="""\
            import typing
            if typing.TYPE_CHECKING:
               from PyQt5.QtWebEngineWidgets import QWebEngineHistory
               from PyQt5.QtWebKit import QWebHistory

            HistoryType = typing.Union['QWebEngineHistory', 'QWebHistory']
            """,
            expected_names=[
                Name(lineno=2, name="typing.TYPE_CHECKING"),
                Name(lineno=6, name="QWebEngineHistory"),
                Name(lineno=6, name="QWebHistory"),
                Name(lineno=6, name="typing.Union"),
            ],
            expected_imports=[
                Import(
                    lineno=1,
                    column=1,
                    name="typing",
                    package="typing",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QWebEngineHistory",
                    package="PyQt5.QtWebEngineWidgets",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="QWebHistory",
                    package="PyQt5.QtWebKit",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_union_from(self):
        self.assertUnimportEqual(
            source="""\
            from typing import TYPE_CHECKING, Union
            if TYPE_CHECKING:
               from PyQt5.QtWebEngineWidgets import QWebEngineHistory
               from PyQt5.QtWebKit import QWebHistory

            HistoryType = Union['QWebEngineHistory', 'QWebHistory']
            """,
            expected_names=[
                Name(lineno=2, name="TYPE_CHECKING"),
                Name(lineno=6, name="QWebEngineHistory"),
                Name(lineno=6, name="QWebHistory"),
                Name(lineno=6, name="Union"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="TYPE_CHECKING",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=1,
                    column=2,
                    name="Union",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QWebEngineHistory",
                    package="PyQt5.QtWebEngineWidgets",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="QWebHistory",
                    package="PyQt5.QtWebKit",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_union_attribute(self):
        self.assertUnimportEqual(
            source="""\
            from typing import TYPE_CHECKING, Union
            if TYPE_CHECKING:
               from PyQt5 import QtWebEngineWidgets
               from PyQt5 import QtWebKit

            HistoryType = Union['QtWebEngineWidgets.QWebEngineHistory', 'QtWebKit.QWebHistory']

            """,
            expected_names=[
                Name(lineno=2, name="TYPE_CHECKING"),
                Name(lineno=6, name="QtWebEngineWidgets.QWebEngineHistory"),
                Name(lineno=6, name="QtWebKit.QWebHistory"),
                Name(lineno=6, name="Union"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="TYPE_CHECKING",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=1,
                    column=2,
                    name="Union",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QtWebEngineWidgets",
                    package="PyQt5",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=4,
                    column=1,
                    name="QtWebKit",
                    package="PyQt5",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_cast_import(self):
        self.assertUnimportEqual(
            source="""\
            import typing
            if typing.TYPE_CHECKING:
               from PyQt5.QtWebKit import QWebHistory

            HistoryType = typing.cast('QWebHistory', None)

            """,
            expected_names=[
                Name(lineno=2, name="typing.TYPE_CHECKING"),
                Name(lineno=5, name="QWebHistory"),
                Name(lineno=5, name="typing.cast"),
            ],
            expected_imports=[
                Import(
                    lineno=1,
                    column=1,
                    name="typing",
                    package="typing",
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QWebHistory",
                    package="PyQt5.QtWebKit",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_cast_from(self):
        self.assertUnimportEqual(
            source="""\
            from typing import TYPE_CHECKING
            if TYPE_CHECKING:
               from PyQt5.QtWebKit import QWebHistory

            HistoryType = cast('QWebHistory', return_value)

            """,
            expected_names=[
                Name(lineno=2, name="TYPE_CHECKING"),
                Name(lineno=5, name="QWebHistory"),
                Name(lineno=5, name="cast"),
                Name(lineno=5, name="return_value"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="TYPE_CHECKING",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QWebHistory",
                    package="PyQt5.QtWebKit",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_cast_attribute(self):
        self.assertUnimportEqual(
            source="""\
            from typing import TYPE_CHECKING
            if TYPE_CHECKING:
               from PyQt5 import QtWebKit

            HistoryType = cast('QtWebKit.QWebHistory', return_value)

            """,
            expected_names=[
                Name(lineno=2, name="TYPE_CHECKING"),
                Name(lineno=5, name="QtWebKit.QWebHistory"),
                Name(lineno=5, name="cast"),
                Name(lineno=5, name="return_value"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="TYPE_CHECKING",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="QtWebKit",
                    package="PyQt5",
                    star=False,
                    suggestions=[],
                ),
            ],
        )


class TestCall(ScannerTestCase):
    def test_call_in_name(self):
        self.assertUnimportEqual(
            source="""\
            from pathlib import Path
            CURRENT_DIR = Path(__file__).parent
            """,
            expected_names=[
                Name(lineno=2, name="Path"),
                Name(lineno=2, name="__file__"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="Path",
                    package="pathlib",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_call_in_attr(self):
        self.assertUnimportEqual(
            source="""\
            a(b.c).d
            """,
            expected_names=[
                Name(lineno=1, name="a"),
                Name(lineno=1, name="b.c"),
            ],
        )

    def test_call_in_str_attr(self):
        self.assertUnimportEqual(
            source="""\
            a("b.c").d
            """,
            expected_names=[
                Name(lineno=1, name="a"),
            ],
        )

    def test_attr_in_call_in_attr(self):
        self.assertUnimportEqual(
            source="""\
            a.b(c.d).f
            """,
            expected_names=[
                Name(lineno=1, name="a.b"),
                Name(lineno=1, name="c.d"),
            ],
        )
