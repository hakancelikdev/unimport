import argparse
import os
import pathlib
import tokenize

from unimport.config import Config
from unimport.files import get_files
from unimport.unused import filter_unused_imports, get_unused


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
            help="Prints a diff of all the changes unimport would make to a file.",
        )
        return parser.parse_args()

    def run(self):
        args = self.parse_args()
        config = Config(config_file=args.config)
        py_files = get_files(args.source, config=config)
        if args.write:
            for py_file in py_files:
                self.overwrite(py_file, get_unused_imports(py_file))
        elif args.diff:
            for py_file in py_files:
                for diff in self.show_diff(py_file):
                    print(diff)
        else:
            for py_file in py_files:
                for unused_import in get_unused_imports(py_file):
                    print(unused_import)

    def overwrite(self, file_path, unused_imports):
        with tokenize.open(file_path) as stream:
            source = stream.read()
            encoding = stream.encoding
        unused_imports = [
            unused_import["name"] for unused_import in unused_imports
        ]
        destination = filter_unused_imports(
            source=source, unused_imports=unused_imports
        )
        pathlib.Path(file_path).write_text(destination, encoding=encoding)


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
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    console_scripts()
