import textwrap
import unittest

from unimport.analyzer import Analyzer
from unimport.constants import PY38_PLUS
from unimport.statement import Import, ImportFrom, Name


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


class NamesTestCase(AnalyzerTestCase):
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
            expected_names=[
                Name(lineno=1, name="variable"),
                Name(lineno=2, name="variable1"),
            ],
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
            expected_names=[Name(lineno=1, name="variable")],
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
            expected_names=[Name(lineno=1, name="variable")],
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
            expected_names=[Name(lineno=1, name="variable")],
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

    def test_normal_name_all_defined_top(self):
        self.assertUnimportEqual(
            source="""\
            __all__ = ["x"]
            import x
            """,
            expected_names=[
                Name(lineno=1, name="__all__"),
                Name(lineno=1, name="x", is_all=True),
            ],
            expected_imports=[
                Import(lineno=2, column=1, name="x", package="x")
            ],
        )


class StarImportTestCase(AnalyzerTestCase):
    include_star_import = True

    def test_star(self):
        self.assertUnimportEqual(
            """\
            from os import *
            __all__ = ["walk", "removedirs"]
            """,
            expected_names=[
                Name(lineno=2, name="__all__"),
                Name(lineno=2, name="walk", is_all=True),
                Name(lineno=2, name="removedirs", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["removedirs", "walk"],
                )
            ],
        )

    def test_append(self):
        self.assertUnimportEqual(
            """\
            from os import *
            __all__ = ["walk"]
            __all__.append("removedirs")
            """,
            expected_names=[
                Name(lineno=2, name="__all__"),
                Name(lineno=3, name="__all__.append"),
                Name(lineno=2, name="walk", is_all=True),
                Name(lineno=3, name="removedirs", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["removedirs", "walk"],
                )
            ],
        )

    def test_extend(self):
        self.assertUnimportEqual(
            """\
            from os import *
            __all__ = ["walk"]
            __all__.extend(["removedirs"])
            """,
            expected_names=[
                Name(lineno=2, name="__all__"),
                Name(lineno=3, name="__all__.extend"),
                Name(lineno=2, name="walk", is_all=True),
                Name(lineno=3, name="removedirs", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="os",
                    package="os",
                    star=True,
                    suggestions=["removedirs", "walk"],
                )
            ],
        )

    def test_star_unused(self):
        self.assertUnimportEqual(
            """\
            from os import *
            __all__ = ["test"]
            """,
            expected_names=[
                Name(lineno=2, name="__all__"),
                Name(lineno=2, name="test", is_all=True),
            ],
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

    def test_unknown(self):
        self.assertUnimportEqual(
            """\
            from x import *
            __all__ = ["xx"]
            """,
            expected_names=[
                Name(lineno=2, name="__all__"),
                Name(lineno=2, name="xx", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="x",
                    package="x",
                    star=True,
                    suggestions=[],
                )
            ],
        )

    def test_unused(self):
        self.assertUnimportEqual(
            """\
            from os import *
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

    def test_used(self):
        self.assertUnimportEqual(
            """\
            from os import *
            print(walk)
            """,
            expected_names=[
                Name(lineno=2, name="print"),
                Name(lineno=2, name="walk"),
            ],
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

    def test_used_and_unused(self):
        self.assertUnimportEqual(
            """\
            from lib2to3.fixer_util import *
            from lib2to3.pytree import *
            from lib2to3.pgen2 import token
            BlankLine, FromImport, Leaf, Newline, Node
            token.NAME, token.STAR
            """,
            expected_names=[
                Name(lineno=4, name="BlankLine"),
                Name(lineno=4, name="FromImport"),
                Name(lineno=4, name="Leaf"),
                Name(lineno=4, name="Newline"),
                Name(lineno=4, name="Node"),
                Name(lineno=5, name="token.NAME"),
                Name(lineno=5, name="token.STAR"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="lib2to3.fixer_util",
                    package="lib2to3.fixer_util",
                    star=True,
                    suggestions=[
                        "BlankLine",
                        "FromImport",
                        "Leaf",
                        "Newline",
                        "Node",
                        "token",
                    ],
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="lib2to3.pytree",
                    package="lib2to3.pytree",
                    star=True,
                    suggestions=["Leaf", "Node"],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="token",
                    package="lib2to3.pgen2",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_used_and_unused_2(self):
        self.assertUnimportEqual(
            """\
            from lib2to3.fixer_util import *
            from lib2to3.pytree import *
            from lib2to3.pgen2.token import *
            BlankLine, FromImport, Leaf, Newline, Node
            NAME, STAR
            """,
            expected_names=[
                Name(lineno=4, name="BlankLine"),
                Name(lineno=4, name="FromImport"),
                Name(lineno=4, name="Leaf"),
                Name(lineno=4, name="Newline"),
                Name(lineno=4, name="Node"),
                Name(lineno=5, name="NAME"),
                Name(lineno=5, name="STAR"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="lib2to3.fixer_util",
                    package="lib2to3.fixer_util",
                    star=True,
                    suggestions=[
                        "BlankLine",
                        "FromImport",
                        "Leaf",
                        "Newline",
                        "Node",
                    ],
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="lib2to3.pytree",
                    package="lib2to3.pytree",
                    star=True,
                    suggestions=["Leaf", "Node"],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="lib2to3.pgen2.token",
                    package="lib2to3.pgen2.token",
                    star=True,
                    suggestions=["NAME", "STAR"],
                ),
            ],
        )

    def test_defined_all(self):
        self.assertUnimportEqual(
            source="""\
            from ast import *

            __all__ = []
            __all__.append("x")
            """,
            expected_names=[
                Name(lineno=3, name="__all__"),
                Name(lineno=4, name="__all__.append"),
                Name(lineno=4, name="x", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="ast",
                    package="ast",
                    star=True,
                    suggestions=[],
                )
            ],
        )

    def test_defined_class(self):
        self.assertUnimportEqual(
            source="""\
            __all__ = ["NodeVisitor", "parse"]

            from ast import *

            class NodeVisitor:
                ...

            literal_eval

            """,
            expected_names=[
                Name(lineno=1, name="__all__"),
                Name(lineno=8, name="literal_eval"),
                Name(lineno=1, name="NodeVisitor", is_all=True),
                Name(lineno=1, name="parse", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="ast",
                    package="ast",
                    star=True,
                    suggestions=["literal_eval", "parse"],
                )
            ],
        )

    def test_defined_function(self):
        self.assertUnimportEqual(
            source="""\
            from ast import *

            __all__.extend(["NodeVisitor", "parse"])

            def literal_eval():
                ...

            """,
            expected_names=[
                Name(lineno=3, name="__all__.extend"),
                Name(lineno=3, name="NodeVisitor", is_all=True),
                Name(lineno=3, name="parse", is_all=True),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="ast",
                    package="ast",
                    star=True,
                    suggestions=["NodeVisitor", "parse"],
                )
            ],
        )


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


@unittest.skipIf(
    not PY38_PLUS, "This feature is only available for python 3.8."
)
class TypeCommentsTestCase(AnalyzerTestCase):
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


class TypeVariableTestCase(AnalyzerTestCase):
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
                Name(lineno=6, name="HistoryType"),
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
                Name(lineno=6, name="HistoryType"),
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
                Name(lineno=6, name="HistoryType"),
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
                Name(lineno=5, name="HistoryType"),
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
                Name(lineno=5, name="HistoryType"),
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
                Name(lineno=5, name="HistoryType"),
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


class CallTestCase(AnalyzerTestCase):
    def test_call_in_name(self):
        self.assertUnimportEqual(
            source="""\
            from pathlib import Path
            CURRENT_DIR = Path(__file__).parent
            """,
            expected_names=[
                Name(lineno=2, name="CURRENT_DIR"),
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
