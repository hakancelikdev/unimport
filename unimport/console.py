import argparse
import os
import pathlib
import tokenize

from unimport.files import get_files
from unimport.unused import get_unused


class Cli(object):
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Detect or remove unused Python imports."
        )
        parser.add_argument(
            "source",
            default=".",
            nargs="?",
            help="include file or folder to find the unused imports",
        )

        parser.add_argument(
            "-w",
            "--write",
            action="store_true",
            help="remove unused imports automatically",
        )

        return parser.parse_args()

    def run(self):
        args = self.parse_args()
        path = pathlib.Path(args.source)
        if path.is_dir():
            for py_file in get_files(args.source):
                for un_used in get_unused_imports(py_file):
                    print(un_used)
        else:
            if path.suffix == ".py":
                for un_used in get_unused_imports(args.source):
                    print(un_used)


def get_unused_imports(file_path):
    try:
        with tokenize.open(file_path) as f:
            source = f.read()
    except OSError:
        pass
    else:
        for imports in get_unused(source=source):
            imports.update(path=file_path.replace(os.getcwd(), ""))
            yield imports


def console_scripts():
    cli = Cli()
    cli.run()


if __name__ == "__main__":
    console_scripts()
