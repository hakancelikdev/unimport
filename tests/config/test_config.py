import re
import sys
from pathlib import Path
from typing import List

import pytest

from unimport import constants as C
from unimport.color import TERMINAL_SUPPORT_COLOR
from unimport.commands import generate_parser
from unimport.config import Config, ParseConfig

TEST_DIR = Path(__file__).parent / "configs"

pyproject = TEST_DIR / "pyproject.toml"
setup_cfg = TEST_DIR / "setup.cfg"

no_unimport_pyproject = TEST_DIR / "no_unimport" / "pyproject.toml"
no_unimport_setup_cfg = TEST_DIR / "no_unimport" / "setup.cfg"


def test_parse_config_toml_parse():
    config = ParseConfig(config_file=pyproject).parse()

    assert config == {
        "sources": [Path("path1"), Path("path2")],
        "exclude": "__init__.py|tests/",
        "include": "test|test2|tests.py",
        "gitignore": False,
        "remove": False,
        "diff": False,
        "ignore_init": False,
    }


def test_parse_config_cfg_parse():
    config = ParseConfig(config_file=setup_cfg).parse()

    assert config == {
        "sources": [Path("path1"), Path("path2")],
        "exclude": "__init__.py|tests/",
        "include": "test|test2|tests.py",
        "gitignore": False,
        "remove": False,
        "diff": False,
        "ignore_init": False,
    }


def test_parse_config_parse_args_config_setup_cfg():
    parser = generate_parser()
    args = parser.parse_args(
        [
            "--config",
            setup_cfg.as_posix(),
            "--include",
            "tests|env",
            "--remove",
            "--diff",
            "--include-star-import",
        ]
    )
    config: Config = ParseConfig.parse_args(args)

    assert config.sources == [Path(".")]
    assert config.include == "tests|env"
    assert config.exclude == "__init__.py|tests/"
    assert config.gitignore is False
    assert config.remove is True
    assert config.diff is True
    assert config.include_star_import is True
    assert config.permission is False
    assert config.check is False
    assert config.ignore_init is False
    assert config.color == "auto"


@pytest.mark.parametrize(
    "argv, expected_argv, attribute_name",
    [
        (["--exclude", "venv"], "venv", "exclude"),
        (["--include", "package"], "package", "include"),
        (
            ["package", "pakcage-2"],
            [Path("package"), Path("pakcage-2")],
            "sources",
        ),
        (["--gitignore"], True, "gitignore"),
        (["--remove"], True, "remove"),
        (["--diff"], True, "diff"),
        (["--include-star-import"], True, "include_star_import"),
        (["--permission"], True, "permission"),
        (["--check"], True, "check"),
        (["--ignore-init"], True, "ignore_init"),
    ],
)
def test_parse_config_parse_args(
    argv: List[str], expected_argv: str, attribute_name: str
):
    parser = generate_parser()
    args = parser.parse_args(argv)
    config = ParseConfig.parse_args(parser.parse_args(argv))

    assert (
        getattr(config, attribute_name) == expected_argv
    ), f"args: {args}, attribute_name: {attribute_name}"


def test_config_build_default_command_same_with_default_config():
    config = Config()

    assert (
        config.build(args={"exclude": config.exclude}).exclude
        == config.build().exclude
    )


def test_config_build_default_check():
    config = Config.build()

    parser = generate_parser()
    assert config.check is True
    assert Config.build(args={"check": True}).check is True

    assert Config.build(args={"diff": True}).check is False
    assert Config.build(args={"remove": True}).check is False
    assert Config.build(args={"permission": True}).check is False


def test_config_build_default_command_diff():
    config = Config.build()

    parser = generate_parser()

    assert config.diff is False
    assert Config.build(args={"remove": True}).diff is False
    assert Config.build(args={"diff": True}).diff is True
    assert Config.build(args={"permission": True}).diff is True


def test_parse_config_toml_command_check():
    config_context = ParseConfig(pyproject).parse()
    parser = generate_parser()

    assert (
        Config.build(args={"check": True}, config_context=config_context).check
        is True
    )
    assert (
        Config.build(
            args={"gitignore": True},
            config_context=config_context,
        ).check
        is True
    )
    assert (
        Config.build(args={"diff": True}, config_context=config_context).check
        is False
    )
    assert (
        Config.build(
            args={"remove": True}, config_context=config_context
        ).check
        is False
    )
    assert (
        Config.build(
            args={"permission": True},
            config_context=config_context,
        ).check
        is False
    )


def test_no_import_section_toml_parse():
    parsed_config = ParseConfig(config_file=no_unimport_pyproject).parse()
    assert parsed_config == {}

    parser = generate_parser()
    args = parser.parse_args(["--config", no_unimport_pyproject.as_posix()])
    config = ParseConfig.parse_args(args)
    assert config == Config.build()


def test_no_import_section_cfg_parse():
    parsed_config = ParseConfig(config_file=no_unimport_setup_cfg).parse()
    assert parsed_config == {}

    parser = generate_parser()
    args = parser.parse_args(["--config", no_unimport_setup_cfg.as_posix()])
    config = ParseConfig.parse_args(args)
    assert config == Config.build()


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


@pytest.mark.parametrize(
    "option,expected_result",
    [
        ("auto", TERMINAL_SUPPORT_COLOR and sys.stderr.isatty()),
        ("always", True),
        ("never", False),
    ],
)
def test_use_color(option, expected_result):
    assert expected_result == Config._use_color(option)


def test_use_color_none_of_them():
    with pytest.raises(ValueError) as cm:
        Config._use_color("none-of-them")

    assert "none-of-them" in str(cm.value)
