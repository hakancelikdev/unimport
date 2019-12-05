import pathlib
from unittest import TestCase

from unimport.config import DEFAULT_IGNORED_FILES, DEFAULT_IGNORED_FOLDERS, Config

TEST_DIR = pathlib.Path(__file__).parent
TEST_DATA = [
    {
        "config_file": TEST_DIR / "samples" / ".unimport.cfg",
        "section": None,
    },
    {
        "config_file": TEST_DIR / "samples" / "pyproject.toml",
        "section": "tool.unimport",
    },
    {
        "config_file": TEST_DIR / "samples" / "setup.cfg",
        "section": "unimport",
    },
]


class ConfigTest(TestCase):
    def test_find_config(self):
        for datum in TEST_DATA:
            config = Config(config_file=datum["config_file"])
            actual_path, actual_section = config.find_config()
            self.assertEqual(actual_path, datum["config_file"])
            self.assertEqual(actual_section, datum["section"])

    def test_parse_config(self):
        expected_folders = DEFAULT_IGNORED_FOLDERS.copy()
        expected_folders.update({".*(migrations)"})

        expected_files = DEFAULT_IGNORED_FILES.copy()
        expected_files.update({".*(__init__.py)", ".*(settings.py)"})

        for datum in TEST_DATA:
            print(datum["section"])
            config = Config(config_file=datum["config_file"])
            self.assertSetEqual(config.ignored_folders, expected_folders)
            self.assertSetEqual(config.ignored_files, expected_files)
