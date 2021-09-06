import os
import unittest
from pathlib import Path

from tests.utils import get_non_native_linesep, reopenable_temp_file
from unimport import utils
from unimport.analyzer import Analyzer
from unimport.refactor import refactor_string
from unimport.statement import Import


class UtilsTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = True
    source = "\n".join(
        [
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )

    def test_list_paths(self):
        self.assertEqual(len(list(utils.list_paths(Path("tests")))), 33)
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
            unused_imports=list(
                Import.get_unused_imports(self.include_star_import)
            ),
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
            self.assertEqual((source, "utf-8", None), utils.read(tmp_path))

    def test_read_newline_native(self):
        with reopenable_temp_file(self.source, newline=os.linesep) as tmp_path:
            self.assertEqual(
                (self.source, "utf-8", os.linesep),
                utils.read(tmp_path),
            )

    def test_read_newline_nonnative(self):
        non_os_sep = get_non_native_linesep()
        with reopenable_temp_file(self.source, newline=non_os_sep) as tmp_path:
            self.assertEqual(
                (self.source, "utf-8", get_non_native_linesep()),
                utils.read(tmp_path),
            )
