import unittest
from unimport.session import Session
import os


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
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'imp': {
                        'lineno': 1,
                        'name': '*',
                        'node_name': 'import',
                        'star': True,
                        'module': os
                    },
                    'modules': ['walk']
                }
            ],
            list(self.session.scanner.from_import_star()))
