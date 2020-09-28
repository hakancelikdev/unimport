from pathlib import Path
from unittest import TestCase

from unimport.session import Session

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"


class TestConfig(TestCase):
    include = ["test|test2|tests.py"]
    exclude = ["__init__.py|tests/"]
    sources = [Path("path1"), Path("path2")]

    def setUp(self):
        self.config_toml = Session(config_file=pyproject).config
        self.config_cfg = Session(config_file=setup_cfg).config

    def test_toml_attr(self):
        self.assertEqual(self.include, self.config_toml.include)
        self.assertEqual(self.exclude, self.config_toml.exclude)
        self.assertEqual(self.sources, self.config_toml.sources)
        self.assertTrue(self.config_toml.gitignore)
        self.assertTrue(self.config_toml.requirements)
        self.assertFalse(self.config_toml.remove)
        self.assertTrue(self.config_toml.diff)

    def test_cfg_attr(self):
        self.assertEqual(self.include, self.config_cfg.include)
        self.assertEqual(self.exclude, self.config_cfg.exclude)
        self.assertEqual(self.sources, self.config_cfg.sources)
        self.assertTrue(self.config_cfg.gitignore)
        self.assertTrue(self.config_cfg.requirements)
        self.assertFalse(self.config_cfg.remove)
        self.assertTrue(self.config_cfg.diff)

    def test_config_default_values(self):
        config = Session(config_file=None).config
        self.assertFalse(config.include)
        self.assertFalse(config.exclude)
        self.assertFalse(config.sources)
        self.assertFalse(config.gitignore)
        self.assertFalse(config.requirements)
        self.assertFalse(config.remove)
        self.assertFalse(config.diff)
