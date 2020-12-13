from pathlib import Path
from unittest import TestCase

from unimport.config import Config

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"


class TestConfig(TestCase):
    include = "test|test2|tests.py"
    exclude = "__init__.py|tests/"
    sources = [Path("path1"), Path("path2")]

    def test_toml_attr(self):
        config = Config(config_file=pyproject).parse()
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)
        self.assertEqual(self.sources, config.sources)
        self.assertTrue(config.gitignore)
        self.assertTrue(config.requirements)
        self.assertFalse(config.remove)
        self.assertTrue(config.diff)

    def test_cfg_attr(self):
        config = Config(config_file=setup_cfg).parse()
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)
        self.assertEqual(self.sources, config.sources)
        self.assertTrue(config.gitignore)
        self.assertTrue(config.requirements)
        self.assertFalse(config.remove)
        self.assertTrue(config.diff)
