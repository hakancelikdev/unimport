import unittest
from unimport.session import Session
import os


class TestFromImportStar(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def test_get_star_imports(self):
        source = (
            "from os import *\n"
            "#from sys import *\n"
            "#import re\n"
            "variable=1\n"
            "print(walk)\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': '*',
                    'node_name': 'import',
                    'star': True,
                    'module': os,
                    'modules': ['walk'],
                }
            ],
            list(self.session.scanner.get_star_imports())
        )

    def test_get_star_imports_2(self):
        source = (
            "from os import *\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'module': os,
                    'name': '*',
                    'node_name': 'import',
                    'star': True,
                    'modules': []
                }
            ],
            list(self.session.scanner.get_star_imports())
        )
