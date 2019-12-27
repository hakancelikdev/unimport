from unittest import TestCase

from .test_helper import TEST_DIR
from unimport.unused import filter_unused_imports, get_unused


class OverwriteTest(TestCase):
    def test_remove_unused_imports(self):
        for py_file in (TEST_DIR / "samples").glob("*_action.py"):
            source = py_file.read_text()
            unused_imports = [i['name'] for i in get_unused(source=source)]
            source_action = filter_unused_imports(
                source=source, unused_imports=unused_imports,
            )
            source_expected = (
                py_file.parent
                / f"{py_file.name.rstrip('_action.py')}_expected.py"
            ).read_text()
            self.assertNotEqual(source, source_expected)
            self.assertEqual(source_action, source_expected)
