import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence, Set

from unimport import color
from unimport import constants as C
from unimport import emoji, utils
from unimport.analyzer import Analyzer
from unimport.config import CONFIG_FILES, Config, DefaultConfig
from unimport.refactor import refactor_string
from unimport.statement import Import, ImportFrom

__all__ = ["main"]

default_config = DefaultConfig()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="unimport",
        description=C.DESCRIPTION,
        epilog=f"Get rid of all unused imports {emoji.PARTYING_FACE}",
    )
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument(
        "sources",
        default=default_config.sources,
        nargs="*",
        help="Files and folders to find the unused imports.",
        action="store",
        type=Path,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prints which file the unused imports are in.",
        default=default_config.check,
    )
    parser.add_argument(
        "-c",
        "--config",
        default=".",
        help="Read configuration from PATH.",
        metavar="PATH",
        action="store",
        type=Path,
    )
    parser.add_argument(
        "--include",
        help="File include pattern.",
        metavar="include",
        action="store",
        default=default_config.include,
        type=str,
    )
    parser.add_argument(
        "--exclude",
        help="File exclude pattern.",
        metavar="exclude",
        action="store",
        default=default_config.exclude,
        type=str,
    )
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="Exclude .gitignore patterns. if present.",
        default=default_config.gitignore,
    )
    parser.add_argument(
        "--ignore-init",
        action="store_true",
        help="Ignore the __init__.py file.",
        default=default_config.ignore_init,
    )
    parser.add_argument(
        "--include-star-import",
        action="store_true",
        help="Include star imports during scanning and refactor.",
        default=default_config.include_star_import,
    )
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Prints a diff of all the changes unimport would make to a file.",
        default=default_config.diff,
    )
    exclusive_group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="Remove unused imports automatically.",
        default=default_config.remove,
    )
    exclusive_group.add_argument(
        "-p",
        "--permission",
        action="store_true",
        help="Refactor permission after see diff.",
        default=default_config.permission,
    )
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="Include requirements.txt file, You can use it with all other arguments",
        default=default_config.requirements,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Unimport {C.VERSION}",
        help="Prints version of unimport",
    )
    argv = argv if argv is not None else sys.argv[1:]
    args = parser.parse_args(argv)
    config = (
        Config(args.config).parse()
        if args.config and args.config.name in CONFIG_FILES
        else default_config
    )
    config = config.merge(**vars(args))
    unused_modules = set()
    used_packages: Set[str] = set()
    for source_path in config.sources:
        for py_path in utils.list_paths(
            source_path, config.include, config.exclude
        ):
            source, encoding, newline = utils.read(py_path)
            analyzer = Analyzer(
                source=source,
                path=py_path,
                include_star_import=config.include_star_import,
            )
            analyzer.traverse()
            unused_imports = list(
                Import.get_unused_imports(config.include_star_import)
            )
            unused_modules.update({imp.name for imp in unused_imports})
            used_packages.update(
                utils.get_used_packages(Import.imports, unused_imports)
            )
            if config.check:
                for imp in unused_imports:
                    if (
                        isinstance(imp, ImportFrom)
                        and imp.star
                        and imp.suggestions
                    ):
                        context = (
                            color.paint(f"from {imp.name} import *", color.RED)
                            + " -> "
                            + color.paint(
                                f"from {imp.name} import {', '.join(imp.suggestions)}",
                                color.GREEN,
                            )
                        )
                    else:
                        context = color.paint(imp.name, color.YELLOW)
                    print(
                        context
                        + " at "
                        + color.paint(py_path.as_posix(), color.GREEN)
                        + ":"
                        + color.paint(str(imp.lineno), color.GREEN)
                    )
            if any((config.diff, config.remove)):
                refactor_result = refactor_string(
                    source=source,
                    unused_imports=unused_imports,
                )
            if config.diff:
                diff = utils.diff(
                    source=source,
                    refactor_result=refactor_result,
                    fromfile=py_path,
                )
                exists_diff = bool(diff)
                if exists_diff:
                    print(color.difference(diff))
            if config.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{color.paint(str(py_path), color.YELLOW)}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return 1
                elif utils.actiontobool(action):
                    config = config._replace(remove=True)
            if config.remove and source != refactor_result:
                with open(
                    py_path, mode="w", encoding=encoding, newline=newline
                ) as py_file:
                    py_file.write(refactor_result)
                print(
                    f"Refactoring '{color.paint(str(py_path), color.GREEN)}'"
                )
            analyzer.clear()
    if not unused_modules and config.check:
        print(
            color.paint(
                f"{emoji.STAR} Congratulations there is no unused import in your project. {emoji.STAR}",
                color.GREEN,
            )
        )
    if config.requirements:
        for requirements in Path(".").glob("requirements*.txt"):
            source = requirements.read_text()
            copy_source = source.splitlines().copy()
            for index, requirement in enumerate(source.splitlines()):
                module_name = utils.package_name_from_metadata(
                    requirement.split("==")[0]
                )
                if module_name is None:
                    print(color.paint(requirement + " not found", color.RED))
                    continue
                if module_name not in used_packages:
                    copy_source.remove(requirement)
                    if config.check:
                        print(
                            f"{color.paint(requirement, color.CYAN)} at "
                            f"{color.paint(requirements.as_posix(), color.CYAN)}:{color.paint(str(index + 1), color.CYAN)}"
                        )
            refactor_result = "\n".join(copy_source)
            if config.diff:
                diff = utils.diff(
                    source=source,
                    refactor_result=refactor_result,
                    fromfile=requirements,
                )
                exists_diff = bool(diff)
                if exists_diff:
                    print(color.difference(diff))
            if config.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{color.paint(requirements.as_posix(), color.CYAN)}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return 1
                if utils.actiontobool(action):
                    config = config._replace(remove=True)
            if config.remove:
                requirements.write_text(refactor_result)
                print(
                    f"Refactoring '{color.paint(requirements.as_posix(), color.CYAN)}'"
                )
    if unused_modules:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
