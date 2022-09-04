import argparse
import contextlib
import io
import textwrap
from pathlib import Path

import pytest

from unimport.constants import PY39_PLUS


@pytest.fixture(scope="module")
def parser() -> argparse.ArgumentParser:
    from unimport.commands import generate_parser

    return generate_parser()


def test_generate_parser_type(parser: argparse.ArgumentParser):
    assert isinstance(parser, argparse.ArgumentParser)


def test_generate_parser_argument_parser(parser: argparse.ArgumentParser):
    assert parser.prog == "unimport"
    assert parser.usage is None
    assert (
        parser.description
        == "A linter, formatter for finding and removing unused import statements."
    )
    assert parser.formatter_class == argparse.HelpFormatter
    assert parser.conflict_handler == "error"
    assert parser.add_help is True


def test_generate_parser_empty_parse_args(parser: argparse.ArgumentParser):
    assert vars(parser.parse_args(["--color", "never"])) == dict(
        check=False,
        color="never",
        config=Path("."),
        diff=False,
        exclude="^$",
        gitignore=False,
        ignore_init=False,
        include="\\.(py)$",
        include_star_import=False,
        permission=False,
        remove=False,
        sources=[Path(".")],
    )


@pytest.mark.skipif(
    PY39_PLUS, reason="This test should work on versions 3.8 and lower."
)
def test_generate_parser_print_help(parser: argparse.ArgumentParser):
    # NOTE: If this test changes, be sure to update this page https://unimport.hakancelik.dev/#command-line-options

    with contextlib.redirect_stdout(io.StringIO()) as f:
        parser.print_help()
    help_message = f.getvalue()

    assert help_message == textwrap.dedent(
        """\
    usage: unimport [-h] [--color {auto,always,never}] [--check] [-c PATH]
                    [--include include] [--exclude exclude] [--gitignore]
                    [--ignore-init] [--include-star-import] [-d] [-r | -p] [-v]
                    [sources [sources ...]]

    A linter, formatter for finding and removing unused import statements.
    
    positional arguments:
      sources               Files and folders to find the unused imports.
    
    optional arguments:
      -h, --help            show this help message and exit
      --color {auto,always,never}
                            Select whether to use color in the output. Defaults to
                            `auto`.
      --check               Prints which file the unused imports are in.
      -c PATH, --config PATH
                            Read configuration from PATH.
      --include include     File include pattern.
      --exclude exclude     File exclude pattern.
      --gitignore           Exclude .gitignore patterns. if present.
      --ignore-init         Ignore the __init__.py file.
      --include-star-import
                            Include star imports during scanning and refactor.
      -d, --diff            Prints a diff of all the changes unimport would make
                            to a file.
      -r, --remove          Remove unused imports automatically.
      -p, --permission      Refactor permission after see diff.
      -v, --version         Prints version of unimport
    
    Get rid of all unused imports 🥳
    """
    )
