import re
from pathlib import Path

from unimport import constants as C
from unimport import utils
from unimport.config import Config, DefaultConfig

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"

no_unimport_pyproject = TEST_DIR / "no_unimport" / "pyproject.toml"
no_unimport_setup_cfg = TEST_DIR / "no_unimport" / "setup.cfg"


def test_config_toml_parse():
    include = "test|test2|tests.py"
    exclude = "__init__.py|tests/"
    sources = [Path("path1"), Path("path2")]

    config = Config(config_file=pyproject).parse()

    assert include == config.include
    assert exclude == config.exclude
    assert sources == config.sources

    assert config.gitignore is True
    assert config.requirements is True
    assert config.diff is True
    assert config.ignore_init is True

    assert config.remove is False


def test_config_cfg_parse():
    include = "test|test2|tests.py"
    exclude = "__init__.py|tests/"
    sources = [Path("path1"), Path("path2")]

    config = Config(config_file=setup_cfg).parse()

    assert include == config.include
    assert exclude == config.exclude
    assert sources == config.sources

    assert config.gitignore is True
    assert config.requirements is True
    assert config.diff is True
    assert config.ignore_init is True

    assert config.remove is False


def test_config_cfg_merge():
    sources = [Path("path1"), Path("path2")]

    config = Config(config_file=setup_cfg).parse()
    console_configuration = {
        "include": "tests|env",
        "remove": True,
        "diff": False,
        "include_star_import": True,
    }
    gitignore_exclude = utils.get_exclude_list_from_gitignore()
    exclude = "|".join(
        [config.exclude] + gitignore_exclude + [C.INIT_FILE_IGNORE_REGEX]
    )
    config = config.merge(**console_configuration)

    assert config.include == "tests|env"
    assert config.exclude == exclude
    assert config.sources == sources

    assert config.gitignore is True
    assert config.requirements is True
    assert config.remove is True

    assert config.diff is False
    assert config.ignore_init is True


def test_default_command__there_is_no_command():
    config = DefaultConfig()

    assert config.merge(there_is_no_command=True) == config.merge()


def test_default_command__same_with_default_config():
    config = DefaultConfig()

    assert (
        config.merge(exclude=config.exclude).exclude == config.merge().exclude
    )


def test_default_command__check():
    config = DefaultConfig()

    assert config.merge().check is True
    assert config.merge(check=True).check is True
    assert config.merge(gitignore=True).check is True

    assert config.merge(diff=True).check is False
    assert config.merge(remove=True).check is False
    assert config.merge(permission=True).check is False


def test_default_command__diff():
    config = DefaultConfig()
    assert config.merge().diff is False
    assert config.merge(remove=True).diff is False

    assert config.merge(diff=True).diff is True
    assert config.merge(permission=True).diff is True


def test_toml_command_same_with_config():
    config = Config(pyproject).parse()
    exclude = "__init__.py|tests/"

    assert config.merge(exclude=exclude).exclude == config.merge().exclude


def test_toml_command_check():
    config = Config(pyproject).parse()

    assert config.merge(check=True).check is True
    assert config.merge(diff=False).check is True
    assert config.merge(diff=False, permission=False).check is True

    assert config.merge().check is False
    assert config.merge(gitignore=True).check is False
    assert config.merge(diff=True).check is False
    assert config.merge(remove=True).check is False
    assert config.merge(permission=True).check is False


def test_no_import_section_toml_parse():
    default_config = DefaultConfig()
    config = Config(config_file=no_unimport_pyproject).parse()

    assert default_config.include == config.include
    assert default_config.exclude == config.exclude
    assert default_config.sources == config.sources
    assert config.gitignore is False
    assert config.requirements is False
    assert config.remove is False
    assert config.diff is False
    assert config.ignore_init is False


def test_no_import_section_cfg_parse():
    default_config = DefaultConfig()
    config = Config(config_file=no_unimport_setup_cfg).parse()

    assert default_config.include == config.include
    assert default_config.exclude == config.exclude
    assert default_config.sources == config.sources
    assert config.gitignore is False
    assert config.requirements is False
    assert config.remove is False
    assert config.diff is False
    assert config.ignore_init is False


def test_no_import_section_cfg_merge():
    default_config = DefaultConfig()
    config = Config(config_file=no_unimport_setup_cfg).parse()
    console_configuration = {
        "include": "tests|env",
        "remove": True,
        "diff": False,
        "include_star_import": True,
    }
    config = config.merge(**console_configuration)

    assert config.include == "tests|env"
    assert default_config.exclude == config.exclude
    assert default_config.sources == config.sources

    assert config.remove is True
    assert config.include_star_import is True

    assert config.gitignore is False
    assert config.requirements is False
    assert config.diff is False


def test_init_file_ignore_regex_match():
    exclude_regex = re.compile(C.INIT_FILE_IGNORE_REGEX)

    assert exclude_regex.search("path/to/__init__.py") is not None
    assert exclude_regex.search("to/__init__.py") is not None
    assert exclude_regex.search("__init__.py") is not None


def test_init_file_ignore_regex_not_match():
    exclude_regex = re.compile(C.INIT_FILE_IGNORE_REGEX)

    assert exclude_regex.search("path/to/_init_.py") is None
    assert exclude_regex.search("path/to/__init__/test.py") is None
    assert exclude_regex.search("__init__") is None
    assert exclude_regex.search("__init__py") is None
    assert exclude_regex.search("__init__bpy") is None
