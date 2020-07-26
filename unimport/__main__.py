import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple

from unimport import __description__, __version__
from unimport.color import Color
from unimport.session import Session

if TYPE_CHECKING:
    from unimport.models import TYPE_IMPORT

parser = argparse.ArgumentParser(
    prog="unimport",
    description=__description__,
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
    version=f"Unimport {__version__}",
    help="Prints version of unimport",
)


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


def get_as_import_from(
    import_name: str, is_star: bool, modules: List[str]
) -> Optional[str]:
    _modules = ""
    if is_star:
        _modules = ", ".join(modules)
        if len(_modules) > 5:
            _modules = "(" + _modules + ")"
    if modules:
        return f"from {import_name} import {_modules}"
    return None


def show(unused_import: "List[TYPE_IMPORT]", py_path: Path) -> None:
    for imp in unused_import:
        import_from = get_as_import_from(
            imp["name"], imp["star"], imp["modules"]
        )
        if (imp["star"] and imp["module"]) or (not imp["star"]):
            print(
                f"{Color(imp['name']).yellow} at "
                f"{Color(str(py_path)).green}:{Color(str(imp['lineno'])).green}"
                f" {import_from or ''}"
            )


def main(argv: Optional[List[str]] = None) -> None:
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
    is_unused_module = False
    unused_modules = set()
    for source_path in namespace.sources:
        for py_path in session.list_paths(source_path, include, exclude):
            session.scanner.run_visit(source=session.read(py_path)[0])
            unused_imports = session.scanner.unused_imports
            if not is_unused_module and unused_imports:
                is_unused_module = True
            unused_modules.update(
                {
                    imp["module"].__name__.split(".")[0]  # type: ignore
                    for imp in unused_imports
                    if imp["module"]
                }
            )
            session.scanner.clear()
            if namespace.check:
                show(unused_imports, py_path)
            if namespace.diff:
                exists_diff = print_if_exists(session.diff_file(py_path))
            if namespace.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{Color(str(py_path)).yellow}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    return
                elif action == "y" or action == "":
                    namespace.remove = True
            if namespace.remove:
                source = session.read(py_path)[0]
                refactor_source = session.refactor_file(py_path, apply=True)
                if refactor_source != source:
                    print(f"Refactoring '{Color(str(py_path)).green}'")
    if not is_unused_module and namespace.check:
        print(
            Color(
                "✨ Congratulations there is no unused import in your project. ✨"
            ).green
        )
    if namespace.requirements and unused_modules:
        requirements_path = Path("requirements.txt")
        if not requirements_path.exists():
            return
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


if __name__ == "__main__":
    main(sys.argv[1:])
