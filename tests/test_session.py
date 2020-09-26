import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from unimport.session import Session


@contextmanager
def reopenable_temp_file(content: str) -> Iterator[Path]:
    """Reopenable tempfile to support writing/reading to/from the opened
    tempfile (requiered for Windows OS).

    For more information: https://bit.ly/3cr0Qkl

    :param content: string content to write.
    :yields: tempfile path.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", encoding="utf-8", delete=False
        ) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(content)
        yield tmp_path
    finally:
        os.unlink(tmp_path)


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
        with reopenable_temp_file(source) as tmp_path:
            result, _ = self.session.refactor_file(path=tmp_path, apply=apply)
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
        with reopenable_temp_file("import os") as tmp_path:
            diff_file = self.session.diff_file(path=tmp_path)
            diff = (
                f"--- {tmp_path.as_posix()}\n",
                "+++ \n",
                "@@ -1 +0,0 @@\n",
                "-import os",
            )
            self.assertEqual(diff, diff_file)

    def test_read(self):
        source = "b�se"
        with reopenable_temp_file(source) as tmp_path:
            self.assertEqual((source, "utf-8"), self.session.read(tmp_path))
