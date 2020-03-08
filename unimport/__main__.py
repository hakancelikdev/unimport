import argparse
import pathlib
import sys

from unimport import __version__
from unimport.session import Session

parser = argparse.ArgumentParser(
    description="Detect or remove unused Python imports."
)
exclusive_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument(
    "sources",
    default=".",
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


def print_if_exists(sequence):
    if sequence:
        print(*sequence, sep="\n")
        return True


def main(argv=None):
    namespace = parser.parse_args(argv)
    any_namespace = any([value for key, value in vars(namespace).items()][2:])
    if namespace.permission and not namespace.diff:
        namespace.diff = True
    session = Session(config_file=namespace.config)
    for source_path in namespace.sources:
        for py_path in session._list_paths(source_path, "**/*.py"):
            if not any_namespace or namespace.check:
                session.scanner.run_visit(source=session._read(py_path)[0])
                for imports in session.scanner.get_unused_imports():
                    if imports["star"]:
                        modules = f"used imports; {imports['modules']}, "
                    else:
                        modules = ""
                    print(
                        f"lineno; {imports['lineno']}, "
                        f"name; \033[93m{imports['name']}\033[00m, "
                        f"{modules}"
                        f"path; \033[92m{str(py_path)}\033[00m ,line {imports['lineno']})"
                    )

                session.scanner.clear()
            if namespace.diff:
                exists_diff = print_if_exists(
                    tuple(session.diff_file(py_path))
                )
                if namespace.permission and exists_diff:
                    action = input(
                        f"Apply suggested changes to \033[92m'{py_path}'\033[00m [y/n/q] ? >"
                    )
                    if action == "q":
                        break
                    elif action == "y":
                        namespace.remove = True
            if namespace.remove:
                session.refactor_file(py_path, apply=True)


if __name__ == "__main__":
    main(sys.argv[1:])
