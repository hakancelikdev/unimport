import tokenize
from unittest import TestCase

from unimport.auto_refactor import refactor
from unimport.unused import get_unused

from .test_helper import TEST_DIR


class OverwriteTest(TestCase):
    def test_remove_unused_imports(self):
        for py_file in (TEST_DIR / "samples").glob("*_action.py"):
            with self.subTest(filename=py_file):
                with tokenize.open(py_file) as stream:
                    source = stream.read()
                unused_imports = [
                    unused_import["name"]
                    for unused_import in get_unused(source=source)
                ]
                source_action = refactor(source, unused_imports,)
                source_expected = (
                    py_file.parent
                    / f"{py_file.name.rstrip('action.py')}expected.py"
                ).read_text()
                self.assertEqual(source_expected, source_action)
