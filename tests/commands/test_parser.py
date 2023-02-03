import argparse
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def parser() -> argparse.ArgumentParser:
    from unimport.commands import generate_parser

    return generate_parser()


def test_generate_parser_type(parser: argparse.ArgumentParser):
    assert isinstance(parser, argparse.ArgumentParser)


def test_generate_parser_argument_parser(parser: argparse.ArgumentParser):
    assert parser.prog == "unimport"
    assert parser.usage is None
    assert parser.description == "A linter, formatter for finding and removing unused import statements."
    assert parser.formatter_class == argparse.HelpFormatter
    assert parser.conflict_handler == "error"
    assert parser.add_help is True


def test_generate_parser_empty_parse_args(parser: argparse.ArgumentParser):
    assert vars(parser.parse_args(["--disable-auto-discovery-config", "--color", "never"])) == dict(
        check=False,
        color="never",
        config=None,
        diff=False,
        disable_auto_discovery_config=True,
        exclude="^$",
        gitignore=False,
        ignore_init=False,
        include="\\.(py)$",
        include_star_import=False,
        permission=False,
        remove=False,
        sources=[Path(".")],
    )
