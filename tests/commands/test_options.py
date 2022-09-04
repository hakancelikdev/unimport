import argparse

import pytest

from unimport.commands import options


@pytest.fixture()
def parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser()


def test_add_sources_option(parser: argparse.ArgumentParser):
    from pathlib import Path

    options.add_sources_option(parser)

    assert vars(parser.parse_args([])) == dict(sources=[Path(".")])


def test_add_check_option(parser: argparse.ArgumentParser):
    options.add_check_option(parser)

    assert vars(parser.parse_args([])) == dict(check=False)
    assert vars(parser.parse_args(["--check"])) == dict(check=True)


def test_add_config_option(parser: argparse.ArgumentParser):
    from pathlib import Path

    options.add_config_option(parser)

    assert vars(parser.parse_args([])) == dict(config=Path("."))
    assert vars(parser.parse_args(["-c", "config.toml"])) == dict(
        config=Path("config.toml")
    )
    assert vars(parser.parse_args(["--config", "config.toml"])) == dict(
        config=Path("config.toml")
    )


def test_add_include_option(parser: argparse.ArgumentParser):
    options.add_include_option(parser)

    assert vars(parser.parse_args([])) == dict(include="\\.(py)$")
    assert vars(
        parser.parse_args(["--include", "tests|datasets|t.py"])
    ) == dict(include="tests|datasets|t.py")


def test_add_exclude_option(parser: argparse.ArgumentParser):
    options.add_exclude_option(parser)

    assert vars(parser.parse_args([])) == dict(exclude="^$")
    assert vars(
        parser.parse_args(["--exclude", "tests|datasets|t.py"])
    ) == dict(exclude="tests|datasets|t.py")


def test_add_gitignore_option(parser: argparse.ArgumentParser):
    options.add_gitignore_option(parser)

    assert vars(parser.parse_args([])) == dict(gitignore=False)
    assert vars(parser.parse_args(["--gitignore"])) == dict(gitignore=True)


def test_add_ignore_init_option(parser: argparse.ArgumentParser):
    options.add_ignore_init_option(parser)

    assert vars(parser.parse_args([])) == dict(ignore_init=False)
    assert vars(parser.parse_args(["--ignore-init"])) == dict(ignore_init=True)


def test_add_include_star_import_option(parser: argparse.ArgumentParser):
    options.add_include_star_import_option(parser)

    assert vars(parser.parse_args([])) == dict(include_star_import=False)
    assert vars(parser.parse_args(["--include-star-import"])) == dict(
        include_star_import=True
    )


def test_add_diff_option(parser: argparse.ArgumentParser):
    options.add_diff_option(parser)

    assert vars(parser.parse_args([])) == dict(diff=False)
    assert vars(parser.parse_args(["-d"])) == dict(diff=True)
    assert vars(parser.parse_args(["--diff"])) == dict(diff=True)


def test_add_remove_option(parser: argparse.ArgumentParser):
    options.add_remove_option(parser)  # type: ignore

    assert vars(parser.parse_args([])) == dict(remove=False)
    assert vars(parser.parse_args(["-r"])) == dict(remove=True)
    assert vars(parser.parse_args(["--remove"])) == dict(remove=True)


def test_add_permission_option(parser: argparse.ArgumentParser):
    options.add_permission_option(parser)  # type: ignore

    assert vars(parser.parse_args([])) == dict(permission=False)
    assert vars(parser.parse_args(["-p"])) == dict(permission=True)
    assert vars(parser.parse_args(["--permission"])) == dict(permission=True)
