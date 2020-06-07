import os
import sys
import typing
import unittest
from typing import Any, Dict, List, Union

from unimport.session import Session

PY38_PLUS = sys.version_info >= (3, 8)


class ScannerTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self) -> None:
        self.scanner = Session(
            include_star_import=self.include_star_import
        ).scanner

    def assertUnimportEqual(
        self,
        source: str,
        expected_names: List[Dict[str, Union[int, str]]],
        expected_classes: List[Dict[str, Union[int, str]]],
        expected_functions: List[Dict[str, Union[int, str]]],
        expected_imports: List[Any],
    ) -> None:
        self.scanner.run_visit(source)
        self.assertEqual(expected_names, self.scanner.names)
        self.assertEqual(expected_classes, self.scanner.classes)
        self.assertEqual(expected_functions, self.scanner.functions)
        self.assertEqual(expected_imports, self.scanner.imports)
        self.scanner.clear()


class TestNames(ScannerTestCase):
    def test_names(self) -> None:
        source = (
            "variable = 1\n"
            "variable1 = 2\n"
            "class TestClass:\n"
            "\tpass\n"
            "def function():\n"
            "\tpass"
        )
        expected_names = [
            {"lineno": 1, "name": "variable",},
            {"lineno": 2, "name": "variable1",},
        ]
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_classes=[{"lineno": 3, "name": "TestClass"}],
            expected_functions=[{"lineno": 5, "name": "function"}],
            expected_imports=[],
        )

    def test_names_with_import(self) -> None:
        source = (
            "variable = 1\n"
            "import os\n"
            "class TestClass():\n"
            "\tdef test_function(self):\n"
            "\t\tpass\n"
            "def test_function():\n"
            "\tpass"
        )
        expected_imports = [
            {
                "lineno": 2,
                "name": "os",
                "star": False,
                "module": os,
                "modules": [],
            },
        ]
        self.assertUnimportEqual(
            source,
            expected_names=[{"lineno": 1, "name": "variable"}],
            expected_classes=[{"lineno": 3, "name": "TestClass"}],
            expected_functions=[{"lineno": 6, "name": "test_function"}],
            expected_imports=expected_imports,
        )

    def test_names_with_function(self) -> None:
        self.assertUnimportEqual(
            source="variable = 1\n" "def test():\n" "\tpass",
            expected_names=[{"lineno": 1, "name": "variable"}],
            expected_classes=[],
            expected_functions=[{"lineno": 2, "name": "test"}],
            expected_imports=[],
        )

    def test_names_with_class(self) -> None:
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
            expected_names=[{"lineno": 1, "name": "variable"}],
            expected_classes=[{"lineno": 4, "name": "test"}],
            expected_functions=[{"lineno": 2, "name": "test_function"}],
            expected_imports=[],
        )

    def test_decator_in_class(self) -> None:
        source = (
            "class Test:\n"
            "    def test(self):\n"
            "        def test2():\n"
            "            return 'test2'\n"
            "        return test2\n"
        )

        self.assertUnimportEqual(
            source,
            expected_names=[{"lineno": 5, "name": "test2"}],
            expected_classes=[{"lineno": 1, "name": "Test"}],
            expected_functions=[],
            expected_imports=[],
        )


class SkipImportTest(ScannerTestCase):
    def assertUnimportEqual(
        self,
        source: str,
        expected_names: List[Any] = [],
        expected_classes: List[Any] = [],
        expected_functions: List[Any] = [],
        expected_imports: List[Any] = [],
    ) -> None:

        super().assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
        )

    def test_inside_try_except(self) -> None:
        source = (
            "try:\n"
            "   import django # unimport:skip\n"
            "except ImportError:\n"
            "   print('install django')\n"
        )
        self.assertUnimportEqual(source)

    def test_as_import(self) -> None:
        source = "from x import y as z # unimport:skip\n"
        self.assertUnimportEqual(source)

    def test_ongoing_comment(self) -> None:
        source = "import unimport # unimport:skip import test\n"
        self.assertUnimportEqual(source)

    def test_skip_comment_second_option(self) -> None:
        source = "import x # unimport:skip test\n"
        self.assertUnimportEqual(source)

    def test_noqa_skip_comment(self) -> None:
        source = "from x import (t, y, f, r) # noqa\n"
        self.assertUnimportEqual(source)

    def test_noqa_skip_comment_multiple(self) -> None:
        source = "from x import ( # noqa\n" "   t, y,\n" "   f, r\n" ")\n"
        self.assertUnimportEqual(source)


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
            {"lineno": 1, "name": "Any"},
            {"lineno": 1, "name": "Union"},
            {"lineno": 1, "name": "Tuple"},
            {"lineno": 1, "name": "Tuple"},
        ]
        expected_classes = []
        expected_functions = [{"lineno": 4, "name": "function"}]
        expected_imports = [
            {
                "lineno": 1,
                "module": typing,
                "modules": [],
                "name": "Any",
                "star": False,
            },
            {
                "lineno": 2,
                "module": typing,
                "modules": [],
                "name": "Tuple",
                "star": False,
            },
            {
                "lineno": 3,
                "module": typing,
                "modules": [],
                "name": "Union",
                "star": False,
            },
        ]
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
        )
