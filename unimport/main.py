import argparse
import sys
from typing import Optional, Sequence, Set

from unimport import color, commands
from unimport import constants as C
from unimport import emoji, utils
from unimport.analyzer import Analyzer
from unimport.commands import options
from unimport.config import Config
from unimport.refactor import refactor_string
from unimport.statement import Import

__all__ = ("main",)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="unimport",
        description=C.DESCRIPTION,
        epilog=f"Get rid of all unused imports {emoji.PARTYING_FACE}",
    )
    exclusive_group = parser.add_mutually_exclusive_group(required=False)

    options.add_sources_option(parser)
    options.add_check_option(parser)
    options.add_config_option(parser)
    color.add_color_option(parser)
    options.add_include_option(parser)
    options.add_exclude_option(parser)
    options.add_gitignore_option(parser)
    options.add_ignore_init_option(parser)
    options.add_include_star_import_option(parser)
    options.add_diff_option(parser)
    options.add_remove_option(exclusive_group)
    options.add_permission_option(exclusive_group)
    options.add_requirements_option(parser)
    options.add_version_option(parser)

    argv = argv if argv is not None else sys.argv[1:]
    args = parser.parse_args(argv)
    config = Config.get_config(args)

    unused_modules = set()
    used_packages: Set[str] = set()

    for path in config.get_paths():
        source, encoding, newline = utils.read(path)

        with Analyzer(
            source=source,
            path=path,
            include_star_import=config.include_star_import,
        ):
            unused_imports = list(
                Import.get_unused_imports(config.include_star_import)
            )
            unused_modules.update({imp.name for imp in unused_imports})
            used_packages.update(
                utils.get_used_packages(Import.imports, unused_imports)
            )
            if config.check:
                commands.check(path, unused_imports, args.color)
            if any((config.diff, config.remove)):
                refactor_result = refactor_string(
                    source=source,
                    unused_imports=unused_imports,
                )
                if config.diff:
                    exists_diff = commands.diff(path, source, refactor_result)
                if config.permission and exists_diff:
                    commands.permission(
                        path, encoding, newline, refactor_result, args.color
                    )
                if config.remove and source != refactor_result:
                    commands.remove(
                        path, encoding, newline, refactor_result, args.color
                    )

    if not unused_modules and config.check:
        print(
            color.paint(
                f"{emoji.STAR} Congratulations there is no unused import in your project. {emoji.STAR}",
                color.GREEN,
                args.color,
            )
        )
    if config.requirements:
        for path in config.get_requirements():
            source = path.read_text()
            copy_source = source.splitlines().copy()

            for index, requirement in enumerate(source.splitlines()):
                module_name = utils.package_name_from_metadata(
                    requirement.split("==")[0]
                )
                if module_name is None:
                    print(
                        color.paint(
                            requirement + " not found", color.RED, args.color
                        )
                    )
                    continue

                if module_name not in used_packages:
                    copy_source.remove(requirement)

                    if config.check:
                        commands.requirements_check(
                            path, index, requirement, args.color
                        )

            refactor_result = "\n".join(copy_source)
            if config.diff:
                exists_diff = commands.diff(path, source, refactor_result)
                if config.permission and exists_diff:
                    commands.requirements_permission(
                        path, refactor_result, args.color
                    )
                if config.remove and source != refactor_result:
                    commands.requirements_remove(
                        path, refactor_result, args.color
                    )

    if unused_modules:
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
