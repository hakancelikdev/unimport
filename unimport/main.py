import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple

from unimport import color
from unimport import constants as C
from unimport.session import Session
from unimport.statement import ImportFrom
from unimport.utils import (
    actiontobool,
    get_exclude_list_from_gitignore,
    get_used_packages,
    package_name_from_metadata,
)


def print_if_exists(sequence: Tuple[str, ...]) -> bool:
    if sequence:
        print(color.difference(sequence))
    return bool(sequence)


def show(unused_import: List[C.ImportT], py_path: Path) -> None:
    for imp in unused_import:
        if isinstance(imp, ImportFrom) and imp.star and imp.suggestions:
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


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="unimport",
        description=C.DESCRIPTION,
        epilog="Get rid of all unused imports 🥳",
    )
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument(
        "sources",
        default=[Path(".")],
        nargs="*",
        help="files and folders to find the unused imports.",
        action="store",
        type=Path,
    )
    parser.add_argument(
        "-c",
        "--config",
        default=".",
        help="read configuration from PATH.",
        metavar="PATH",
        action="store",
        type=Path,
    )
    parser.add_argument(
        "--include",
        help="file include pattern.",
        metavar="include",
        action="store",
        default=[],
        type=lambda value: [value],
    )
    parser.add_argument(
        "--exclude",
        help="file exclude pattern.",
        metavar="exclude",
        action="store",
        default=[],
        type=lambda value: [value],
    )
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="exclude .gitignore patterns. if present.",
    )
    parser.add_argument(
        "--include-star-import",
        action="store_true",
        help="Include star imports during scanning and refactor.",
    )
    parser.add_argument(
        "--show-error",
        action="store_true",
        help="Show or don't show errors captured during static analysis.",
    )
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Prints a diff of all the changes unimport would make to a file.",
    )
    exclusive_group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="remove unused imports automatically.",
    )
    exclusive_group.add_argument(
        "-p",
        "--permission",
        action="store_true",
        help="Refactor permission after see diff.",
    )
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="Include requirements.txt file, You can use it with all other arguments",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prints which file the unused imports are in.",
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
    session = Session(
        config_file=args.config,
        include_star_import=args.include_star_import,
        show_error=args.show_error,
    )
    args.remove = args.remove or session.config.remove  # type: ignore
    args.diff = any((args.diff, args.permission, session.config.diff))  # type: ignore
    args.check = args.check or not any((args.diff, args.remove))
    args.requirements = args.requirements or session.config.requirements  # type: ignore
    args.gitignore = args.gitignore or session.config.gitignore  # type: ignore
    args.sources.extend(session.config.sources)  # type: ignore
    args.include.extend(session.config.include)  # type: ignore
    args.exclude.extend(session.config.exclude)  # type: ignore
    if args.gitignore:
        args.exclude.extend(get_exclude_list_from_gitignore())
    include = re.compile("|".join(args.include)).pattern
    exclude = re.compile("|".join(args.exclude)).pattern
    unused_modules = set()
    packages: Set[str] = set()
    for source_path in args.sources:
        for py_path in session.list_paths(source_path, include, exclude):
            session.scanner.scan(source=session.read(py_path)[0])
            unused_imports = session.scanner.unused_imports
            unused_modules.update({imp.name for imp in unused_imports})
            packages.update(
                get_used_packages(
                    session.scanner.imports, session.scanner.unused_imports
                )
            )
            if args.check:
                show(unused_imports, py_path)
            session.scanner.clear()
            if args.diff:
                exists_diff = print_if_exists(session.diff_file(py_path))
            if args.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{color.paint(str(py_path), color.YELLOW)}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return 1
                elif actiontobool(action):
                    args.remove = True
            if args.remove and session.refactor_file(py_path, apply=True)[1]:
                print(
                    f"Refactoring '{color.paint(str(py_path), color.GREEN)}'"
                )
    if not unused_modules and args.check:
        print(
            color.paint(
                "✨ Congratulations there is no unused import in your project. ✨",
                color.GREEN,
            )
        )
    if args.requirements and packages:
        for requirements in Path(".").glob("requirements*.txt"):
            splitlines_requirements = requirements.read_text().splitlines()
            result = splitlines_requirements.copy()
            for index, requirement in enumerate(splitlines_requirements):
                module_name = package_name_from_metadata(
                    requirement.split("==")[0]
                )
                if module_name is None:
                    if args.show_error:
                        print(
                            color.paint(requirement + " not found", color.RED)
                        )
                    continue
                if module_name not in packages:
                    result.remove(requirement)
                    if args.check:
                        print(
                            f"{color.paint(requirement, color.CYAN)} at "
                            f"{color.paint(requirements.as_posix(), color.CYAN)}:{color.paint(str(index + 1), color.CYAN)}"
                        )
            if args.diff:
                exists_diff = print_if_exists(
                    tuple(
                        difflib.unified_diff(
                            splitlines_requirements,
                            result,
                            fromfile=requirements.as_posix(),
                        )
                    )
                )
            if args.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{color.paint(requirements.as_posix(), color.CYAN)}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return 1
                if actiontobool(action):
                    args.remove = True
            if args.remove:
                requirements.write_text("".join(result))
                print(
                    f"Refactoring '{color.paint(requirements.as_posix(), color.CYAN)}'"
                )
    if unused_modules:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
