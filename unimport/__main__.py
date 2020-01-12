import argparse
import pathlib
import sys

from unimport.session import Session

parser = argparse.ArgumentParser(
    description="Detect or remove unused Python imports."
)
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
    help="read configuration from PATH.",
    metavar="PATH",
    type=pathlib.Path,
)
parser.add_argument(
    "-w",
    "--write",
    action="store_true",
    help="remove unused imports automatically.",
)
parser.add_argument(
    "-d",
    "--diff",
    action="store_true",
    help="Prints a diff of all the changes unimport would make to a file.",
)


def print_if_exists(sequence):
    if sequence:
        print(*sequence, sep="\n")
        return True


def main(argv=None):
    namespace = parser.parse_args(argv)
    session = Session(config_file=namespace.config)
    sources = []
    for source in namespace.sources:
        sources.extend(session._list_paths(source, "**/*.py"))

    if namespace.diff and namespace.write:
        for source in sources:
            print_if_exists(tuple(session.diff_file(source)))
            session.refactor_file(source, apply=True)
    elif namespace.diff:
        for source in sources:
            diff = tuple(session.diff_file(source))
            if print_if_exists(diff):
                action = input(
                    f"Apply suggested changes to '{source}' [y/n/q] ? > "
                )
                if action == "q":
                    break
                elif action == "y":
                    session.refactor_file(source, apply=True)
    elif namespace.write:
        for source in sources:
            session.refactor_file(source, apply=True)
    else:
        for source in sources:
            print_if_exists(tuple(session.scan_file(source)))

    print("All done!")


if __name__ == "__main__":
    main(sys.argv[1:])
