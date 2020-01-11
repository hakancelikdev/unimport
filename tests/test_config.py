from unittest import TestCase

from .test_helper import TEST_DIR
from unimport.config import (
    Config,
    DEFAULT_EXCLUDES
)

TEST_DATA = [
    {
        "config_file": TEST_DIR / "samples" / "configs" / "pyproject.toml",
        "section": "tool.unimport",
    },
    {
        "config_file": TEST_DIR / "samples" / "configs" / "setup.cfg",
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
        expected_exclude = DEFAULT_EXCLUDES.copy()
        expected_exclude.update({"./[0-9].*", "tests"})
        for datum in TEST_DATA:
            config = Config(config_file=datum["config_file"])
            self.assertSetEqual(config.exclude, expected_exclude)
