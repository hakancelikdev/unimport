import argparse
import pathlib
import sys

from unimport import __description__, __version__
from unimport.color import Color
from unimport.session import Session

parser = argparse.ArgumentParser(description=__description__)
exclusive_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument(
    "sources",
    default=[pathlib.Path(".")],
    nargs="*",
    help="files and folders to find the unused imports.",
    type=pathlib.Path,
)
parser.add_argument(
    "-c",
    "--config",
    default=".",
    help="read configuration from PATH.",
    metavar="PATH",
    type=pathlib.Path,
)
parser.add_argument(
    "--include-star-import",
    action="store_true",
    help="Include star imports during scanning and refactor.",
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


def print_if_exists(sequence):
    if sequence:
        print(color_diff(sequence))
        return True


def output(name, path, lineno, modules):
    return (
        f"{Color(name).yellow} at "
        f"{Color(str(path)).green}:{Color(str(lineno)).green}"
        f" {modules}"
    )


def get_modules(is_star: bool, modules: str) -> str:
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
    return modules


def show(unused_import: list, py_path: str) -> None:
    if not unused_import:
        print(
            Color(
                "🐍 🕵️‍♂️ ✨ Congratulations there is no unused import in your project. ✨ 🕵️‍♂️ 🐍"
            ).green
        )
    for imp in unused_import:
        if (
            (imp["star"] and imp["module"])
            or (not imp["star"] and imp["module"])
            and (not imp["star"] and not imp["module"])
        ):
            print(
                output(
                    imp["name"],
                    py_path,
                    imp["lineno"],
                    get_modules(imp["star"], imp["modules"]),
                )
            )


def main(argv=None):
    namespace = parser.parse_args(argv)
    any_namespace = any([value for key, value in vars(namespace).items()][3:])
    session = Session(
        config_file=namespace.config,
        include_star_import=namespace.include_star_import,
    )
    for source_path in namespace.sources:
        for py_path in session._list_paths(source_path, "**/*.py"):
            if not any_namespace or namespace.check:
                session.scanner.run_visit(source=session._read(py_path)[0])
                show(list(session.scanner.get_unused_imports()), py_path)
                session.scanner.clear()
            if namespace.diff or namespace.permission:
                exists_diff = print_if_exists(session.diff_file(py_path))
            if namespace.permission and exists_diff:
                action = input(
                    f"Apply suggested changes to '{Color(str(py_path)).yellow}' [y/n/q] ? >"
                )
                if action == "q":
                    break
                elif action == "y":
                    namespace.remove = True
            if namespace.remove:
                source = session._read(py_path)[0]
                refactor_source = session.refactor_file(py_path, apply=True)
                if refactor_source != source:
                    print(f"Refactoring '{Color(str(py_path)).green}'")


if __name__ == "__main__":
    main(sys.argv[1:])
