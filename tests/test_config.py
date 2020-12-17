from pathlib import Path
from unittest import TestCase

from unimport import utils
from unimport.config import Config, DefaultConfig

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"

no_unimport_pyproject = TEST_DIR / "no_unimport" / "pyproject.toml"
no_unimport_setup_cfg = TEST_DIR / "no_unimport" / "setup.cfg"


class TestConfig(TestCase):
    include = "test|test2|tests.py"
    exclude = "__init__.py|tests/"
    sources = [Path("path1"), Path("path2")]

    def test_toml_parse(self):
        config = Config(config_file=pyproject).parse()
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)
        self.assertEqual(self.sources, config.sources)
        self.assertTrue(config.gitignore)
        self.assertTrue(config.requirements)
        self.assertFalse(config.remove)
        self.assertTrue(config.diff)

    def test_cfg_parse(self):
        config = Config(config_file=setup_cfg).parse()
        self.assertEqual(self.include, config.include)
        self.assertEqual(self.exclude, config.exclude)
        self.assertEqual(self.sources, config.sources)
        self.assertTrue(config.gitignore)
        self.assertTrue(config.requirements)
        self.assertFalse(config.remove)
        self.assertTrue(config.diff)

    def test_cfg_merge(self):
        config = Config(config_file=setup_cfg).parse()
        console_configuration = {
            "include": "tests|env",
            "remove": True,
            "diff": False,
            "include_star_import": True,
        }
        gitignore_exclude = utils.get_exclude_list_from_gitignore()
        gitignore_exclude.extend(config.exclude)
        exclude = "|".join(gitignore_exclude)
        config = config.merge(**console_configuration)
        self.assertEqual("tests|env", config.include)
        self.assertEqual(exclude, config.exclude)
        self.assertEqual(self.sources, config.sources)
        self.assertTrue(config.gitignore)
        self.assertTrue(config.requirements)
        self.assertTrue(config.remove)
        self.assertFalse(config.diff)


class TestDefaultCommand(TestCase):
    def setUp(self):
        self.config = DefaultConfig()

    def test_there_is_no_command(self):
        self.assertEqual(
            self.config.merge(ther_is_no_command=True), self.config.merge()
        )

    def test_same_with_default_config(self):
        self.assertEqual(
            self.config.merge(exclude=self.config.exclude).exclude,
            self.config.merge().exclude,
        )

    def test_check(self):
        self.assertTrue(self.config.merge().check)
        self.assertTrue(self.config.merge(check=True).check)
        self.assertTrue(self.config.merge(gitignore=True).check)

        self.assertFalse(self.config.merge(diff=True).check)
        self.assertFalse(self.config.merge(remove=True).check)
        self.assertFalse(self.config.merge(permission=True).check)

    def test_diff(self):
        self.assertFalse(self.config.merge().diff)
        self.assertFalse(self.config.merge(remove=True).diff)

        self.assertTrue(self.config.merge(diff=True).diff)
        self.assertTrue(self.config.merge(permission=True).diff)


class TestTomlCommand(TestCase):
    def setUp(self):
        self.config = Config(pyproject).parse()
        self.exclude = "__init__.py|tests/"

    def test_same_with_toml_config(self):
        self.assertEqual(
            self.config.merge(exclude=self.exclude).exclude,
            self.config.merge().exclude,
        )

    def test_check(self):
        self.assertTrue(self.config.merge(check=True).check)
        self.assertTrue(self.config.merge(diff=False).check)
        self.assertTrue(self.config.merge(diff=False, permission=False).check)

        self.assertFalse(self.config.merge().check)
        self.assertFalse(self.config.merge(gitignore=True).check)
        self.assertFalse(self.config.merge(diff=True).check)
        self.assertFalse(self.config.merge(remove=True).check)
        self.assertFalse(self.config.merge(permission=True).check)


class TestNoUnimportSectionTest(TestCase):
    def setUp(self):
        self.default_config = DefaultConfig()

    def test_toml_parse(self):
        config = Config(config_file=no_unimport_pyproject).parse()
        self.assertEqual(self.default_config.include, config.include)
        self.assertEqual(self.default_config.exclude, config.exclude)
        self.assertEqual(self.default_config.sources, config.sources)
        self.assertFalse(config.gitignore)
        self.assertFalse(config.requirements)
        self.assertFalse(config.remove)
        self.assertFalse(config.diff)

    def test_cfg_parse(self):
        config = Config(config_file=no_unimport_setup_cfg).parse()
        self.assertEqual(self.default_config.include, config.include)
        self.assertEqual(self.default_config.exclude, config.exclude)
        self.assertEqual(self.default_config.sources, config.sources)
        self.assertFalse(config.gitignore)
        self.assertFalse(config.requirements)
        self.assertFalse(config.remove)
        self.assertFalse(config.diff)

    def test_cfg_merge(self):
        config = Config(config_file=no_unimport_setup_cfg).parse()
        console_configuration = {
            "include": "tests|env",
            "remove": True,
            "diff": False,
            "include_star_import": True,
        }
        config = config.merge(**console_configuration)
        self.assertEqual("tests|env", config.include)
        self.assertEqual(self.default_config.exclude, config.exclude)
        self.assertEqual(self.default_config.sources, config.sources)

        self.assertTrue(config.remove)
        self.assertTrue(config.include_star_import)

        self.assertFalse(config.gitignore)
        self.assertFalse(config.requirements)
        self.assertFalse(config.diff)
