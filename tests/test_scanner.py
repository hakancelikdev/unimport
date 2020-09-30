import unittest

from unimport.constants import PY38_PLUS
from unimport.scan import ImportableVisitor
from unimport.session import Session
from unimport.statement import Import, ImportFrom, Name


class ScannerTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self):
        self.scanner = Session(
            include_star_import=self.include_star_import
        ).scanner

    def assertUnimportEqual(
        self,
        source,
        expected_names=[],
        expected_imports=[],
    ):
        self.scanner.scan(source)
        self.assertEqual(expected_names, self.scanner.names)
        self.assertEqual(expected_imports, self.scanner.imports)
        self.scanner.clear()


class TestNames(ScannerTestCase):
    def test_names(self):
        source = (
            "variable = 1\n"
            "variable1 = 2\n"
            "class TestClass:\n"
            "\tpass\n"
            "def function():\n"
            "\tpass"
        )
        self.assertUnimportEqual(
            source,
            expected_names=[
                Name(lineno=1, name="variable"),
                Name(lineno=2, name="variable1"),
            ],
        )

    def test_names_with_import(self):
        source = (
            "variable = 1\n"
            "import os\n"
            "class TestClass():\n"
            "\tdef test_function(self):\n"
            "\t\tpass\n"
            "def test_function():\n"
            "\tpass"
        )
        self.assertUnimportEqual(
            source,
            expected_names=[Name(lineno=1, name="variable")],
            expected_imports=[Import(lineno=2, column=1, name="os")],
        )

    def test_names_with_function(self):
        self.assertUnimportEqual(
            source="variable = 1\n" "def test():\n" "\tpass",
            expected_names=[Name(lineno=1, name="variable")],
        )

    def test_names_with_class(self):
        source = (
            "variable = 1\n"
            "def test_function():\n"
            "\tpass\n"
            "class test():\n"
            "\tdef test_function():\n"
            "\t\tpass"
        )
        self.assertUnimportEqual(
            source,
            expected_names=[Name(lineno=1, name="variable")],
        )

    def test_decator_in_class(self):
        source = (
            "class Test:\n"
            "    def test(self):\n"
            "        def test2():\n"
            "            return 'test2'\n"
            "        return test2\n"
        )

        self.assertUnimportEqual(
            source,
            expected_names=[Name(lineno=5, name="test2")],
        )


class SkipImportTest(ScannerTestCase):
    def assertSkipEqual(self, source):
        super().assertUnimportEqual(
            source,
        )

    def test_inside_try_except(self):
        source = (
            "try:\n"
            "   import django # unimport:skip\n"
            "except ImportError:\n"
            "   print('install django')\n"
        )
        self.assertSkipEqual(source)

    def test_as_import(self):
        source = "from x import y as z # unimport:skip\n"
        self.assertSkipEqual(source)

    def test_ongoing_comment(self):
        source = "import unimport # unimport:skip import test\n"
        self.assertSkipEqual(source)

    def test_skip_comment_second_option(self):
        source = "import x # unimport:skip test\n"
        self.assertSkipEqual(source)

    def test_noqa_skip_comment(self):
        source = "from x import (t, y, f, r) # noqa\n"
        self.assertSkipEqual(source)

    def test_noqa_skip_comment_multiple(self):
        source = "from x import ( # noqa\n" "   t, y,\n" "   f, r\n" ")\n"
        self.assertSkipEqual(source)

    def test_skip_file(self):
        source = "# unimport:skip_file\n" "import x\n"
        self.assertSkipEqual(source)

    def test_skip_file_after_import(self):
        source = "import x\n" "# unimport:skip_file\n"
        self.assertSkipEqual(source)


@unittest.skipIf(
    not PY38_PLUS, "This feature is only available for python 3.8."
)
class TestTypeComments(ScannerTestCase):
    def test_type_comments(self):
        source = (
            "from typing import Any\n"
            "from typing import Tuple\n"
            "from typing import Union\n"
            "def function(a, b):\n"
            "    # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]\n"
            "    pass\n"
        )
        expected_names = [
            Name(lineno=1, name="Any"),
            Name(lineno=1, name="Union"),
            Name(lineno=1, name="Tuple"),
            Name(lineno=1, name="Tuple"),
        ]
        expected_imports = [
            ImportFrom(
                lineno=1, column=1, name="Any", star=False, suggestions=[]
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="Tuple",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3, column=1, name="Union", star=False, suggestions=[]
            ),
        ]
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_imports,
        )


class TestImportable(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.importable = ImportableVisitor()

    def test_get_names_from_all(self):
        source = (
            "__all__ = ['test']\n"
            "__all__.append('test2')\n"
            "__all__.extend(['test3'])\n"
            "\n"
        )
        expected = frozenset({"test3", "test", "test2"})
        self.importable.traverse(source)
        self.assertEqual(expected, self.importable.get_all())

    def test_get_names_from_suggestion(self):
        source = (
            "import xx\n"
            "class A:\n"
            "   pass\n"
            "def b():\n"
            "   FUNCNAME = 'test'\n"
            "NAME='NAME'\n"
            "\n"
        )
        expected = frozenset({"xx", "NAME", "b", "A"})
        self.importable.traverse(source)
        self.assertEqual(expected, self.importable.get_suggestion())


class TestTypeVariable(ScannerTestCase):
    def test_type_assing_union(self):
        source = (
            "import typing\n"
            "if typing.TYPE_CHECKING:\n"
            "   from PyQt5.QtWebEngineWidgets import QWebEngineHistory\n"
            "   from PyQt5.QtWebKit import QWebHistory\n"
            "\n"
            "HistoryType = typing.Union['QWebEngineHistory', 'QWebHistory']\n"
            "\n"
        )
        expected_names = [
            Name(lineno=2, name="typing.TYPE_CHECKING"),
            Name(lineno=2, name="typing"),
            Name(lineno=6, name="HistoryType"),
            Name(lineno=6, name="QWebEngineHistory"),
            Name(lineno=6, name="QWebHistory"),
            Name(lineno=6, name="typing.Union"),
            Name(lineno=6, name="typing"),
        ]
        expected_imports = [
            Import(lineno=1, column=1, name="typing"),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebEngineHistory",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="QWebHistory",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_names, expected_imports)

        source = (
            "from typing import TYPE_CHECKING, Union\n"
            "if TYPE_CHECKING:\n"
            "   from PyQt5.QtWebEngineWidgets import QWebEngineHistory\n"
            "   from PyQt5.QtWebKit import QWebHistory\n"
            "\n"
            "HistoryType = Union['QWebEngineHistory', 'QWebHistory']\n"
            "\n"
        )

        expected_names = [
            Name(lineno=2, name="TYPE_CHECKING"),
            Name(lineno=6, name="HistoryType"),
            Name(lineno=6, name="QWebEngineHistory"),
            Name(lineno=6, name="QWebHistory"),
            Name(lineno=6, name="Union"),
        ]
        expected_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="TYPE_CHECKING",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1, column=2, name="Union", star=False, suggestions=[]
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebEngineHistory",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="QWebHistory",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_names, expected_imports)
