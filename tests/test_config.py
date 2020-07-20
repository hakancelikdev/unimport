from pathlib import Path
from unittest import TestCase

from unimport import config as CONFIG
from unimport.session import Session

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
        self.config_toml = Session(
            config_file=CONFIG_TOML["config_file"]
        ).config
        self.config_cfg = Session(config_file=CONFIG_CFG["config_file"]).config

    def test_toml_attr(self):
        self.assertEqual(self.include, self.config_toml.include)
        self.assertEqual(self.exclude, self.config_toml.exclude)

    def test_toml_is_available_to_parse(self):
        setattr(CONFIG, "HAS_TOML", True)
        self.assertTrue(
            self.config_toml.is_available_to_parse(
                self.config_toml.config_file
            )
        )

    def test_toml_but_has_toml_false(self):
        setattr(CONFIG, "HAS_TOML", False)
        self.assertFalse(
            self.config_toml.is_available_to_parse(
                self.config_toml.config_file
            )
        )

    def test_cfg_attr(self):
        self.assertEqual(self.include, self.config_cfg.include)
        self.assertEqual(self.exclude, self.config_cfg.exclude)

    def test_cfg_is_available_to_parse(self):
        self.assertTrue(
            self.config_cfg.is_available_to_parse(self.config_cfg.config_file)
        )

    def test_config_file_none(self):
        none_config = Session(config_file=None).config
        self.assertIsNone(none_config)
