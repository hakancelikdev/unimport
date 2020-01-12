import tokenize
from unittest import TestCase

from unimport.session import Session

from .test_helper import TEST_DIR


class OverwriteTest(TestCase):
    def setUp(self):
        self.session = Session()

    def test_remove_unused_imports(self):
        for py_file in (TEST_DIR / "samples").glob("*_action.py"):
            with self.subTest(filename=py_file):
                source_action = self.session.refactor_file(py_file)
                source_expected = (
                    py_file.parent
                    / f"{py_file.name.rstrip('action.py')}expected.py"
                ).read_text()
                self.assertEqual(source_expected, source_action)
