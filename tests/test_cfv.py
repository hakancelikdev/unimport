import unittest
from unimport.scan import Scanner

import os

class TestNames(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_names(self):
        source = (
            "variable = 1\n"
            "variable1 = 2\n"
            "class TestClass:\n"
            "\tpass\n"
            "def function():\n"
            "\tpass"
        )
        self.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': 'variable',
                },
                {
                    'lineno': 2,
                    'name': 'variable1',
                },
            ],

            self.scanner.names
        )
        self.assertEqual([], self.scanner.imports)
        self.assertEqual([{'lineno': 3, 'name': 'TestClass'}], self.scanner.classes)
        self.assertEqual([{'lineno': 5, 'name': 'function'}], self.scanner.functions)

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
        self.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': 'variable',
                },
            ],
            self.scanner.names
        )
        self.assertEqual(
            [
                {
                    'lineno': 2,
                    'name': 'os',
                    'star': False,
                    'module': os
                },
            ],
            self.scanner.imports
        )
        self.assertEqual([{'lineno': 3, 'name': 'TestClass'}], self.scanner.classes)
        self.assertEqual([{'lineno': 6, 'name': 'test_function'}], self.scanner.functions)

    def test_names_with_function(self):
        source = (
            "variable = 1\n"
            "def test():\n"
            "\tpass"
        )
        self.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': 'variable',
                },
            ],
            Scanner(source).names
        )
        self.assertEqual([], self.scanner.imports)
        self.assertEqual([], self.scanner.classes)

        self.assertEqual(
            [
                {
                    'lineno': 2,
                    'name': 'test',
                },
            ],
            self.scanner.functions)

    def test_names_with_class(self):
        source = (
            "variable = 1\n"
            "def test_function():\n"
            "\tpass\n"
            "class test():\n"
            "\tdef test_function():\n"
            "\t\tpass"
        )
        self.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': 'variable',
                },
            ],
            self.scanner.names
        )
        self.assertEqual([], self.scanner.imports)
        self.assertEqual(
            [
                {
                    'lineno': 4,
                    'name': 'test',
                },
            ],
            self.scanner.classes)
        self.assertEqual([{'lineno': 2, 'name': 'test_function'}],  self.scanner.functions)
