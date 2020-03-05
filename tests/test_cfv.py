import unittest
from unimport.scan import Scanner

import os

class TestNames(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_names(self):
        source = (
            "variable = 1\n"
            "variable1 = 2"
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
                }
            ],

            self.scanner.names
        )
        self.assertEqual([], self.scanner.imports)
        self.assertEqual([], self.scanner.classes)
        self.assertEqual([], self.scanner.functions)

    def test_names_with_import(self):
        source = (
            "variable = 1\n"
            "import os"
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
        self.assertEqual([], self.scanner.classes)
        self.assertEqual([], self.scanner.functions)

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
            "class test():\n"
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
        self.assertEqual([], self.scanner.imports)
        self.assertEqual(
            [
                {
                    'lineno': 2,
                    'name': 'test',
                },
            ],
            self.scanner.classes)
        self.assertEqual([],  self.scanner.functions)
