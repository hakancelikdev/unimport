import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from unimport import utils
from unimport.analyzer import Analyzer
from unimport.refactor import refactor_string


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


class UtilsTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = True

    def test_list_paths(self):
        self.assertEqual(len(list(utils.list_paths(Path("tests")))), 8)
        self.assertEqual(
            len(list(utils.list_paths(Path("tests/test_config.py")))), 1
        )

    def refactor(self, path: Path) -> str:
        source = utils.read(path)[0]
        analyzer = Analyzer(
            source=source, include_star_import=self.include_star_import
        )
        analyzer.traverse()
        refactor_result = refactor_string(
            source=analyzer.source,
            unused_imports=list(analyzer.get_unused_imports()),
        )
        return refactor_result

    def temp_refactor(self, source: str, expected: str):
        with reopenable_temp_file(source) as tmp_path:
            self.assertEqual(self.refactor(tmp_path), expected)

    def test_bad_encoding(self):
        # Make conflict between BOM and encoding Cookie.
        # https://docs.python.org/3/library/tokenize.html#tokenize.detect_encoding
        bad_encoding = "\ufeff\n# -*- coding: utf-32 -*-\nbad encoding"
        self.temp_refactor(source=bad_encoding, expected="")

    def test_refactor_file(self):
        self.temp_refactor(source="import os", expected="")

    def test_refactor_file_apply(self):
        self.temp_refactor(source="import os", expected="")

    def test_diff_file(self):
        with reopenable_temp_file("import os") as tmp_path:
            source = utils.read(tmp_path)[0]
            refactor_result = self.refactor(tmp_path)
            diff_file = utils.diff(
                source=source,
                refactor_result=refactor_result,
                fromfile=tmp_path,
            )
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
            self.assertEqual((source, "utf-8"), utils.read(tmp_path))
