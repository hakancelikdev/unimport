import tokenize
from unittest import TestCase

from unimport.unused import filter_unused_imports, get_unused

from .test_helper import TEST_DIR


class OverwriteTest(TestCase):
    def test_remove_unused_imports(self):
        for py_file in (TEST_DIR / "samples").glob("*_action.py"):
            with tokenize.open(py_file) as stream:
                source = stream.read()
            unused_imports = [
                unused_import["name"]
                for unused_import in get_unused(source=source)
            ]
            source_action = filter_unused_imports(
                source=source, unused_imports=unused_imports,
            )
            source_expected = (
                py_file.parent
                / f"{py_file.name.rstrip('action.py')}expected.py"
            ).read_text()
            self.assertNotEqual(source, source_expected)
            self.assertEqual(source_action, source_expected)
