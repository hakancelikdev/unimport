import unittest
from unimport.session import Session

import os

# These imports to write in modules below.
from pathlib import Path
import pathlib
import lib2to3.fixer_util
import lib2to3.pytree
import lib2to3.pgen2.token

class TestUnusedImport(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_unused_import_1(self):
        source = (
            "from pathlib import Path\n"
            "CURRENT_DIR = Path('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual([], list(self.session.scanner.get_unused_imports()))

    def test_unused_import_2(self):
        source = ("from pathlib import Path")
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'module': pathlib,
                    'name': 'Path',
                    'star': False
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )

    def test_unused_import_3(self):
        source = (
            "import x.y\n"
            "import d.f.a.s\n"
            "CURRENT_DIR = x.y('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 2,
                    'module': None,
                    'name': 'd.f.a.s',
                    'star': False
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )

    def test_unused_import_4(self):
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
                    'star': True,
                    'module': os,
                    'modules': ['walk'],
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )

    def test_unused_import_5(self):
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
                    'star': True,
                    'modules': []
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )

    def test_unused_import_6(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2 import token\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "token.NAME, token.STAR\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'module': lib2to3.fixer_util,
                    'name': '*',
                    'star': True,
                    'modules': ["BlankLine", "FromImport", "Leaf", "Newline", "Node", "token", "token.NAME", "token.STAR"]
                },
                {
                    'lineno': 2,
                    'module': lib2to3.pytree,
                    'name': '*',
                    'star': True,
                    'modules': ["Leaf", "Node"]
                },
            ],
            list(self.session.scanner.get_unused_imports())
        )

    def test_unused_import_7(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2.token import *\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "NAME, STAR\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'name': '*',
                    'module': lib2to3.fixer_util,
                    'star': True,
                    'modules': ["BlankLine", "FromImport", "Leaf", "Newline", "Node"]
                },
                {
                    'lineno': 2,
                    'name': '*',
                    'module': lib2to3.pytree,
                    'star': True,
                    'modules': ["Leaf", "Node"]
                },
                {
                    'lineno': 3,
                    'name': '*',
                    'star': True,
                    'module': lib2to3.pgen2.token,
                    'modules': ['NAME', 'STAR']
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )
