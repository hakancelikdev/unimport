import unittest
from unimport.session import Session

import os

class TestUnusedImport(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def test_unused_import_1(self):
        from pathlib import Path
        source = (
            "from pathlib import Path\n"
            "CURRENT_DIR = Path('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual([], list(self.session.scanner.get_unused_imports()))

    def test_unused_import_2(self):
        import pathlib
        source = ("from pathlib import Path")
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    'lineno': 1,
                    'module': pathlib,
                    'name': 'Path',
                    'node_name': 'import',
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
                    'node_name': 'import',
                    'star': False
                }
            ],
            list(self.session.scanner.get_unused_imports())
        )
