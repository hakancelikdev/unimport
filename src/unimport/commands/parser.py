import argparse

from unimport import __description__
from unimport.commands import options
from unimport.enums import Emoji

__all__ = ("generate_parser",)


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unimport",
        description=__description__,
        epilog=f"Get rid of all unused imports {Emoji.PARTYING_FACE}",
    )
    exclusive_group = parser.add_mutually_exclusive_group(required=False)

    options.add_color_option(parser)
    options.add_sources_option(parser)
    options.add_check_option(parser)
    options.add_config_option(parser)
    options.add_include_option(parser)
    options.add_exclude_option(parser)
    options.add_gitignore_option(parser)
    options.add_ignore_init_option(parser)
    options.add_include_star_import_option(parser)
    options.add_diff_option(parser)
    options.add_remove_option(exclusive_group)
    options.add_permission_option(exclusive_group)
    options.add_version_option(parser)

    return parser
