import tempfile
import unittest
from pathlib import Path

from unimport.session import Session


class TestSession(unittest.TestCase):
    maxDiff = None
    include_star_import = True

    def setUp(self) -> None:
        self.session = Session(include_star_import=self.include_star_import)

    def test_list_paths_and_read(self) -> None:
        for path in [Path("tests"), Path("tests/test_config.py")]:
            for p in self.session._list_paths(path):
                self.assertTrue(str(p).endswith(".py"))
                with self.subTest(p=p):
                    self.session._read(p)

    def temp_refactor(
        self, source: bytes, expected: str, apply: bool = False
    ) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as tmp:
            tmp.write(source)
            tmp.seek(0)
            result = self.session.refactor_file(
                path=Path(tmp.name), apply=apply
            )
            self.assertEqual(result, expected)

    def test_refactor_file(self) -> None:
        self.temp_refactor(source="import os", expected="")

    def test_refactor_file_apply(self) -> None:
        self.temp_refactor(source="import os", expected="", apply=True)

    def test_diff(self) -> None:
        diff = ("--- \n", "+++ \n", "@@ -1 +0,0 @@\n", "-import os")
        self.assertEqual(diff, self.session.diff("import os"))

    def test_diff_file(self) -> None:
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

    def test_read_with_bad_syntax(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as tmp:
            tmp.write("b�se")
            tmp.seek(0)
            self.assertEqual(("b�se", "utf-8"), self.session._read(tmp.name))
