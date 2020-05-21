from pathlib import Path
from unittest import TestCase

from unimport.config import Config

TEST_DIR = Path(__file__).parent

CONFIG_TOML = {
    "config_file": TEST_DIR / "configs" / "pyproject.toml",
    "section": "tool.unimport",
}

CONFIG_CFG = {
    "config_file": TEST_DIR / "configs" / "setup.cfg",
    "section": "unimport",
}


CONFIG_PATHS = [CONFIG_TOML, CONFIG_CFG]


class TestConfig(TestCase):
    def setUp(self):
        self.include = "test|test2|tests.py"
        self.exclude = "__init__.py|tests/"

    def test_find_config(self):
        for config_path in CONFIG_PATHS:
            config = Config(config_file=config_path["config_file"])
            actual_path, actual_section = config.find_config()
            self.assertEqual(actual_path, config_path["config_file"])
            self.assertEqual(actual_section, config_path["section"])
            self.assertEqual(self.include, config.include)
            self.assertEqual(self.exclude, config.exclude)
