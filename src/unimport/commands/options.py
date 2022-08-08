import argparse
from pathlib import Path

from unimport import __version__
from unimport.config import Config

__all__ = (
    "add_sources_option",
    "add_check_option",
    "add_config_option",
    "add_include_option",
    "add_exclude_option",
    "add_gitignore_option",
    "add_ignore_init_option",
    "add_include_star_import_option",
    "add_diff_option",
    "add_remove_option",
    "add_permission_option",
    "add_version_option",
)


def add_sources_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "sources",
        default=Config.default_sources,
        nargs="*",
        help="Files and folders to find the unused imports.",
        action="store",
        type=Path,
    )


def add_check_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prints which file the unused imports are in.",
        default=Config.check,
    )


def add_config_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-c",
        "--config",
        default=".",
        help="Read configuration from PATH.",
        metavar="PATH",
        action="store",
        type=Path,
    )


def add_include_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include",
        help="File include pattern.",
        metavar="include",
        action="store",
        default=Config.include,
        type=str,
    )


def add_exclude_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--exclude",
        help="File exclude pattern.",
        metavar="exclude",
        action="store",
        default=Config.exclude,
        type=str,
    )


def add_gitignore_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="Exclude .gitignore patterns. if present.",
        default=Config.gitignore,
    )


def add_ignore_init_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--ignore-init",
        action="store_true",
        help="Ignore the __init__.py file.",
        default=Config.ignore_init,
    )


def add_include_star_import_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-star-import",
        action="store_true",
        help="Include star imports during scanning and refactor.",
        default=Config.include_star_import,
    )


def add_diff_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Prints a diff of all the changes unimport would make to a file.",
        default=Config.diff,
    )


def add_remove_option(
    exclusive_group: argparse._MutuallyExclusiveGroup,
) -> None:
    exclusive_group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="Remove unused imports automatically.",
        default=Config.remove,
    )


def add_permission_option(
    exclusive_group: argparse._MutuallyExclusiveGroup,
) -> None:
    exclusive_group.add_argument(
        "-p",
        "--permission",
        action="store_true",
        help="Refactor permission after see diff.",
        default=Config.permission,
    )


def add_version_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Unimport {__version__}",
        help="Prints version of unimport",
    )


def add_color_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--color",
        default=Config.color,
        type=str,
        metavar="{" + ",".join(Config._get_color_choices()) + "}",
        help="Select whether to use color in the output. Defaults to `%(default)s`.",
    )
