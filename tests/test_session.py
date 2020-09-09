import tempfile
import unittest
from pathlib import Path

from unimport.session import Session


class TestSession(unittest.TestCase):
    maxDiff = None
    include_star_import = True

    def setUp(self):
        self.session = Session(include_star_import=self.include_star_import)

    def test_list_paths_and_read(self):
        for path in [Path("tests"), Path("tests/test_config.py")]:
            for p in self.session.list_paths(path):
                self.assertTrue(str(p).endswith(".py"))

    def temp_refactor(self, source: str, expected: str, apply: bool = False):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as tmp:
            tmp.write(source)
            tmp.seek(0)
            result = self.session.refactor_file(
                path=Path(tmp.name), apply=apply
            )
            self.assertEqual(result, expected)

    def test_bad_encoding(self):
        # Make conflict between BOM and encoding Cookie.
        # https://docs.python.org/3/library/tokenize.html#tokenize.detect_encoding
        bad_encoding = "\ufeff\n# -*- coding: utf-32 -*-\nbad encoding"
        self.temp_refactor(source=bad_encoding, expected="")

    def test_refactor_file(self):
        self.temp_refactor(source="import os", expected="")

    def test_refactor_file_apply(self):
        self.temp_refactor(source="import os", expected="", apply=True)

    def test_diff(self):
        diff = ("--- \n", "+++ \n", "@@ -1 +0,0 @@\n", "-import os")
        self.assertEqual(diff, self.session.diff("import os"))

    def test_diff_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as tmp:
            tmp.write("import os")
            tmp.seek(0)
            diff_file = self.session.diff_file(path=Path(tmp.name))
            diff = (
                f"--- {tmp.name}\n",
                "+++ \n",
                "@@ -1 +0,0 @@\n",
                "-import os",
            )
            self.assertEqual(diff, diff_file)

    def test_read(self):
        source = "b�se"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as tmp:
            tmp.write(source)
            tmp.seek(0)
            self.assertEqual(
                (source, "utf-8"), self.session.read(Path(tmp.name))
            )
