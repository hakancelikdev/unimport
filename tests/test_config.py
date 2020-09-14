from pathlib import Path
from unittest import TestCase

from unimport import config as CONFIG
from unimport.session import Session

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"


class TestConfig(TestCase):
    def setUp(self):
        self.include = "test|test2|tests.py"
        self.exclude = "__init__.py|tests/"
        self.config_toml = Session(config_file=pyproject).config
        self.config_cfg = Session(config_file=setup_cfg).config

    def test_toml_attr(self):
        self.assertEqual(self.include, self.config_toml.include)
        self.assertEqual(self.exclude, self.config_toml.exclude)
        self.assertTrue(self.config_toml.gitignore)

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
        self.assertFalse(self.config_cfg.gitignore)

    def test_cfg_is_available_to_parse(self):
        self.assertTrue(
            self.config_cfg.is_available_to_parse(self.config_cfg.config_file)
        )

    def test_config_file_none(self):
        none_config = Session(config_file=None).config
        self.assertIsNone(none_config)
