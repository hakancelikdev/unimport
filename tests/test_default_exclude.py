import fnmatch
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from unimport.config import DEFAULT_EXCLUDES

from .test_helper import TEST_DIR


class DefaultExclude(TestCase):

    DEFAULT_EXCLUDE_NAMES = [
        ".git",
        ".github",
        "build",
        "__pycache__",
        "develop-eggs",
        "dist",
        "downloads",
        "eggs",
        "lib",
        "lib64",
        "parts",
        "sdist",
        "var",
        "wheels",
        ".egg-info",
        "MANIFEST",
        "htmlcov",
        ".tox",
        ".hypothesis",
        ".pytest_cache",
        "instance",
        "docs",
        "target",
        "celerybeat-schedul",
        ".venv",
        "env",
        "venv",
        "site",
        ".mypy_cache",
        ".sage.py",
        "local_settings.py",
        "__init__.py",
    ]

    def test_exlude_folder(self):
        with TemporaryDirectory() as directory:
            for exclude_name in self.DEFAULT_EXCLUDE_NAMES:
                folder_path = (Path(directory) / exclude_name)
                folder_path.mkdir()
                for pattern_exclude in DEFAULT_EXCLUDES:
                    match = fnmatch.fnmatch(folder_path, pattern_exclude)
                    if match:
                        break
                self.assertTrue(match)

    def test_exlude_files(self):
        with TemporaryDirectory() as directory:
            for exclude_name in self.DEFAULT_EXCLUDE_NAMES:
                folder_path = Path(directory) / exclude_name
                folder_path.mkdir()
                if not str(folder_path).endswith(".py"):
                    file_path = folder_path / "test.py"
                    with file_path.open("a", encoding ="utf-8") as f:
                        f.write("import os")
                    for pattern_exclude in DEFAULT_EXCLUDES:
                        match = fnmatch.fnmatch(file_path, pattern_exclude)
                        if match:
                            break
                    self.assertTrue(match)
