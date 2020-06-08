import argparse
import re
import sys
from pathlib import Path

from unimport import __description__, __version__
from unimport.color import Color
from unimport.session import Session

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


def color_diff(sequence: tuple) -> str:
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


def print_if_exists(sequence: tuple):
    if sequence:
        print(color_diff(sequence))
        return True
    return None


def output(name: str, path: Path, lineno: int, modules: str) -> str:
    modules = modules or ""
    return (
        f"{Color(name).yellow} at "
        f"{Color(str(path)).green}:{Color(str(lineno)).green}"
        f" {modules}"
    )


def get_modules(imp: str, is_star: bool, modules: str):
    if is_star:
        _modules = ", ".join(modules)
        if len(_modules) > 5:
            modules = f"({_modules})"
        elif len(_modules) == 0:
            modules = ""
        else:
            modules = f"{_modules}"
    else:
        modules = ""
    if modules:
        return f"from {imp} import {modules}"
    return None


def show(unused_import, py_path):
    for imp in unused_import:
        modules = get_modules(imp["name"], imp["star"], imp["modules"])
        if (imp["star"] and imp["module"]) or (not imp["star"]):
            print(output(imp["name"], py_path, imp["lineno"], modules,))


def main(argv=None):
    namespace = parser.parse_args(argv)
    namespace.check = namespace.check or not any(
        [value for key, value in vars(namespace).items()][6:-1]
    )
    session = Session(
        config_file=namespace.config,
        include_star_import=namespace.include_star_import,
        show_error=namespace.show_error,
    )
    include_list, exclude_list = [], []
    if namespace.include:
        include_list.append(namespace.include)
    if hasattr(session.config, "include"):
        include_list.append(session.config.include)
    if namespace.exclude:
        exclude_list.append(namespace.exclude)
    if hasattr(session.config, "exclude"):
        exclude_list.append(session.config.exclude)
    include = re.compile("|".join(include_list)).pattern
    exclude = re.compile("|".join(exclude_list)).pattern
    _any_unimport = False
    for source_path in namespace.sources:
        for py_path in session._list_paths(source_path, include, exclude):
            if namespace.check:
                session.scanner.run_visit(source=session._read(py_path)[0])
                unused_imports = session.scanner.unused_imports
                show(unused_imports, py_path)
                if not (not _any_unimport and not unused_imports):
                    _any_unimport = True
                session.scanner.clear()
            if namespace.diff or namespace.permission:
                exists_diff = print_if_exists(session.diff_file(py_path))
            if namespace.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{Color(str(py_path)).yellow}' [Y/n/q] ? >"
                ).lower()
                if action == "q":
                    break
                elif action == "y" or action == "":
                    namespace.remove = True
            if namespace.remove:
                source = session._read(py_path)[0]
                refactor_source = session.refactor_file(py_path, apply=True)
                if refactor_source != source:
                    print(f"Refactoring '{Color(str(py_path)).green}'")
    if not _any_unimport and namespace.check:
        print(
            Color(
                "✨ Congratulations there is no unused import in your project. ✨"
            ).green
        )


if __name__ == "__main__":
    main(sys.argv[1:])
