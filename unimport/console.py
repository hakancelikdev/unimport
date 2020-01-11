import argparse
import difflib
import pathlib
import tokenize

from unimport.auto_refactor import refactor
from unimport.config import Config
from unimport.files import get_files, overwrite
from unimport.unused import get_unused_from_file


class CLI:
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Detect or remove unused Python imports."
        )
        parser.add_argument(
            "source",
            default=".",
            nargs="?",
            help="include file or folder to find the unused imports.",
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
        return parser.parse_args()

    def run(self):
        args = self.parse_args()
        config = Config(config_file=args.config)
        py_files = get_files(args.source, config=config)
        if args.write and args.diff:
            for py_file in py_files:
                unused_imports = list(get_unused_from_file(py_file))
                get_diff = list(context_diff(py_file, unused_imports))
                if get_diff:
                    for diff in get_diff:
                        print(diff)
                    overwrite(py_file, unused_imports)
        elif args.write:
            for py_file in py_files:
                overwrite(py_file, get_unused_from_file(py_file))

        elif args.diff:
            for py_file in py_files:
                unused_imports = list(get_unused_from_file(py_file))
                get_diff = list(context_diff(py_file, unused_imports))
                if get_diff:
                    for diff in get_diff:
                        print(diff)
                    overwrite_permission = input(
                        f"Apply suggested changes to '{py_file}' [y/n/q] ? > "
                    )
                    if overwrite_permission == "y":
                        overwrite(py_file, unused_imports)
                    elif overwrite_permission == "q":
                        break
        else:
            for py_file in py_files:
                for unused_import in get_unused_from_file(py_file):
                    print(unused_import)
        print("All done!")


def context_diff(file_path, unused_imports):
    with tokenize.open(file_path) as stream:
        old_sourcesource = stream.read()
    new_source = refactor(
        old_sourcesource,
        unused_imports=[
            unused_import["name"] for unused_import in unused_imports
        ],
    )
    return difflib.context_diff(
        old_sourcesource.splitlines(), new_source.splitlines()
    )


def console_scripts():
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    console_scripts()
