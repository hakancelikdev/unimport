import unittest
import importlib
import sys
from unimport.scan import Scanner
import inspect
from unimport.session import Session


class TestFromImportStar(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def test_from_import_star(self):
        source = (
            "from os import *\n"
            "#from sys import *\n"
            "#import re\n"
            "variable=1\n"
            "print(walk)\n"
            "execlp"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual([('from os import ', 'walk', 'execlp')], list(self.session.scanner.from_import_star()))
