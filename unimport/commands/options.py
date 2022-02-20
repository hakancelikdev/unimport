import argparse
from pathlib import Path

from unimport import constants as C
from unimport.config import DefaultConfig

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
    "add_requirements_option",
    "add_version_option",
)

default_config = DefaultConfig()


def add_sources_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "sources",
        default=default_config.sources,
        nargs="*",
        help="Files and folders to find the unused imports.",
        action="store",
        type=Path,
    )


def add_check_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prints which file the unused imports are in.",
        default=default_config.check,
    )


def add_config_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-c",
        "--config",
        default=".",
        help="Read configuration from PATH.",
        metavar="PATH",
        action="store",
        type=Path,
    )


def add_include_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--include",
        help="File include pattern.",
        metavar="include",
        action="store",
        default=default_config.include,
        type=str,
    )


def add_exclude_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--exclude",
        help="File exclude pattern.",
        metavar="exclude",
        action="store",
        default=default_config.exclude,
        type=str,
    )


def add_gitignore_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="Exclude .gitignore patterns. if present.",
        default=default_config.gitignore,
    )


def add_ignore_init_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--ignore-init",
        action="store_true",
        help="Ignore the __init__.py file.",
        default=default_config.ignore_init,
    )


def add_include_star_import_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--include-star-import",
        action="store_true",
        help="Include star imports during scanning and refactor.",
        default=default_config.include_star_import,
    )


def add_diff_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Prints a diff of all the changes unimport would make to a file.",
        default=default_config.diff,
    )


def add_remove_option(exclusive_group: argparse._MutuallyExclusiveGroup):
    exclusive_group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="Remove unused imports automatically.",
        default=default_config.remove,
    )


def add_permission_option(exclusive_group: argparse._MutuallyExclusiveGroup):
    exclusive_group.add_argument(
        "-p",
        "--permission",
        action="store_true",
        help="Refactor permission after see diff.",
        default=default_config.permission,
    )


def add_requirements_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="Include requirements.txt file, You can use it with all other arguments",
        default=default_config.requirements,
    )


def add_version_option(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Unimport {C.VERSION}",
        help="Prints version of unimport",
    )
