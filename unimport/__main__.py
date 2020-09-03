import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union

import unimport.constants as C
from unimport.color import Color
from unimport.session import Session
from unimport.statement import Import, ImportFrom


def color_diff(sequence: Tuple[str, ...]) -> str:
    contents = "\n".join(sequence)
    lines = contents.split("\n")
    for i, line in enumerate(lines):
        paint = Color(line)
        if line.startswith("+++") or line.startswith("---"):
            line = paint.bold_white
        if line.startswith("@@"):
            line = paint.cyan
        if line.startswith("+"):
            line = paint.green
        elif line.startswith("-"):
            line = paint.red
        lines[i] = line
    return "\n".join(lines)


def print_if_exists(sequence: Tuple[str, ...]) -> bool:
    if sequence:
        print(color_diff(sequence))
    return bool(sequence)


def show(
    unused_import: List[Union[Import, ImportFrom]], py_path: Path
) -> None:
    for imp in unused_import:
        context = ""
        if (
            isinstance(imp, ImportFrom)
            and imp.star
            and imp.module
            and imp.modules
        ):
            context = (
                Color(f"from {imp.name} import *").red
                + " -> "
                + Color(
                    f"from {imp.name} import {', '.join(imp.modules)}"
                ).green
            )
        else:
            context = Color(imp.name).yellow
        print(
            context
            + " at "
            + Color(str(py_path)).green
            + ":"
            + Color(str(imp.lineno)).green
        )


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
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
        default="",
        type=str,
    )
    parser.add_argument(
        "--exclude",
        help="file exclude pattern.",
        metavar="exclude",
        action="store",
        default="",
        type=str,
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

    namespace = parser.parse_args(argv)
    namespace.check = namespace.check or not any(
        [namespace.diff, namespace.remove, namespace.permission]
    )
    namespace.diff = namespace.diff or namespace.permission
    session = Session(
        config_file=namespace.config,
        include_star_import=namespace.include_star_import,
        show_error=namespace.show_error,
    )
    include_list = []
    exclude_list = []
    if namespace.include:
        include_list.append(namespace.include)
    if hasattr(session.config, "include"):
        include_list.append(session.config.include)  # type: ignore
    if namespace.exclude:
        exclude_list.append(namespace.exclude)
    if hasattr(session.config, "exclude"):
        exclude_list.append(session.config.exclude)  # type: ignore
    include = re.compile("|".join(include_list)).pattern
    exclude = re.compile("|".join(exclude_list)).pattern
    unused_modules = set()
    for source_path in namespace.sources:
        for py_path in session.list_paths(source_path, include, exclude):
            session.scanner.scan(source=session.read(py_path)[0])
            unused_imports = session.scanner.unused_imports
            if unused_imports:
                unused_modules.update(
                    {
                        imp.module.__name__.split(".")[0]  # type: ignore
                        for imp in unused_imports
                        if imp.module
                    }
                )
            if namespace.check:
                show(unused_imports, py_path)
            session.scanner.clear()
            if namespace.diff:
                exists_diff = print_if_exists(session.diff_file(py_path))
            if namespace.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{Color(str(py_path)).yellow}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return 1
                elif action == "y" or action == "":
                    namespace.remove = True
            if namespace.remove:
                source = session.read(py_path)[0]
                refactor_source = session.refactor_file(py_path, apply=True)
                if refactor_source != source:
                    print(f"Refactoring '{Color(str(py_path)).green}'")
    if not unused_modules and namespace.check:
        print(
            Color(
                "✨ Congratulations there is no unused import in your project. ✨"
            ).green
        )
    requirements_path = Path("requirements.txt")
    if (
        namespace.requirements
        and unused_modules
        and requirements_path.exists()
    ):
        result = ""
        source = requirements_path.read_text()
        for index, requirement in enumerate(source.splitlines()):
            if requirement.split("==")[0] not in unused_modules:
                result += f"{requirement}\n"
            else:
                if namespace.check and requirement:
                    print(
                        f"{Color(requirement).cyan} at "
                        f"{Color(str(requirements_path)).cyan}:{Color(str(index + 1)).cyan}"
                    )
        if namespace.diff:
            exists_diff = print_if_exists(
                tuple(
                    difflib.unified_diff(
                        source.splitlines(),
                        result.splitlines(),
                        fromfile=str(requirements_path),
                    )
                )
            )
        if namespace.permission and exists_diff:
            action = input(
                f"Apply suggested changes to '{Color(str(requirements_path)).cyan}' [Y/n] ? >"
            ).lower()
            if action == "y" or action == "":
                namespace.remove = True
        if namespace.remove:
            requirements_path.write_text(result)
            print(f"Refactoring '{Color(str(requirements_path)).cyan}'")
    if unused_modules:
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
