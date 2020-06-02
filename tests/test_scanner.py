import os
import unittest

from unimport.scan import Scanner


class ScannerTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.scanner = Scanner()

    def assertUnimportEqual(
        self,
        source,
        expected_names,
        expected_classes,
        expected_functions,
        expected_imports,
    ):
        self.scanner.run_visit(source)
        self.assertEqual(expected_names, list(self.scanner.get_names()))
        self.assertEqual(expected_classes, self.scanner.classes)
        self.assertEqual(expected_functions, self.scanner.functions)
        self.assertEqual(expected_imports, self.scanner.imports)


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
        expected_names = [
            {"lineno": 1, "name": "variable",},
            {"lineno": 2, "name": "variable1",},
        ]
        expected_classes = [{"lineno": 3, "name": "TestClass"}]
        expected_functions = [{"lineno": 5, "name": "function"}]
        expected_imports = []
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
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
        expected_names = [
            {"lineno": 1, "name": "variable",},
        ]
        expected_classes = [{"lineno": 3, "name": "TestClass"}]
        expected_functions = [{"lineno": 6, "name": "test_function"}]
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
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
        )

    def test_names_with_function(self):
        source = "variable = 1\n" "def test():\n" "\tpass"
        expected_names = [
            {"lineno": 1, "name": "variable"},
        ]
        expected_classes = []
        expected_functions = [
            {"lineno": 2, "name": "test"},
        ]
        expected_imports = []
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
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
        expected_names = [
            {"lineno": 1, "name": "variable"},
        ]
        expected_classes = [
            {"lineno": 4, "name": "test"},
        ]
        expected_functions = [{"lineno": 2, "name": "test_function"}]
        expected_imports = []
        self.assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
        )


class SkipImportTest(ScannerTestCase):
    def assertUnimportEqual(
        self,
        source,
        expected_names=[],
        expected_classes=[],
        expected_functions=[],
        expected_imports=[],
    ):

        super().assertUnimportEqual(
            source,
            expected_names,
            expected_classes,
            expected_functions,
            expected_imports,
        )

    def test_inside_try_except(self):
        source = (
            "try:\n"
            "   import django #unimport:skip\n"
            "except ImportError:\n"
            "   print('install django')\n"
        )
        self.assertUnimportEqual(source,)

    def test_as_import(self):
        source = "from x import y as z #unimport:skip\n"
        self.assertUnimportEqual(source,)

    def test_ongoing_comment(self):
        source = "import unimport #unimport:skip import test\n"
        self.assertUnimportEqual(source,)
