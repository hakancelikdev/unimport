from pathlib import Path
from unittest import TestCase

from unimport import config as CONFIG

Config = CONFIG.Config

TEST_DIR = Path(__file__).parent

CONFIG_TOML = {
    "config_file": TEST_DIR / "configs" / "pyproject.toml",
    "section": "tool.unimport",
}

CONFIG_CFG = {
    "config_file": TEST_DIR / "configs" / "setup.cfg",
    "section": "unimport",
}


class TestConfig(TestCase):
    def setUp(self):
        self.include = "test|test2|tests.py"
        self.exclude = "__init__.py|tests/"

    def test_toml_find_config(self):
        config = Config(config_file=CONFIG_TOML["config_file"])
        actual_path, actual_section = config.find_config()
        self.assertEqual(actual_path, CONFIG_TOML["config_file"])
        self.assertEqual(actual_section, CONFIG_TOML["section"])

    def test_toml_attr(self):
        config = Config(config_file=CONFIG_TOML["config_file"])
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)

    def test_toml_is_available_to_parse(self):
        setattr(CONFIG, "HAS_TOML", True)
        config = Config(config_file=CONFIG_TOML["config_file"])
        self.assertTrue(config.is_available_to_parse(config.config_file))

    def test_toml_but_has_toml_false(self):
        setattr(CONFIG, "HAS_TOML", False)
        config = Config(config_file=CONFIG_TOML["config_file"])
        self.assertFalse(config.is_available_to_parse(config.config_file))

    def test_cfg_find_config(self):
        config = Config(config_file=CONFIG_CFG["config_file"])
        actual_path, actual_section = config.find_config()
        self.assertEqual(actual_path, CONFIG_CFG["config_file"])
        self.assertEqual(actual_section, CONFIG_CFG["section"])

    def test_cfg_attr(self):
        config = Config(config_file=CONFIG_CFG["config_file"])
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)

    def test_cfg_is_available_to_parse(self):
        config = Config(config_file=CONFIG_CFG["config_file"])
        self.assertTrue(config.is_available_to_parse(config.config_file))

    def test_config_file_none_find_config(self):
        config = Config(config_file=None)
        actual_path, actual_section = config.find_config()
        self.assertIsNone(actual_path)
        self.assertIsNone(actual_section)
