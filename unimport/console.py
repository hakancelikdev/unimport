import argparse
import difflib
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
            action="store_true",
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
                unused_imports = get_unused_imports(py_file)
                get_diff = self.context_diff(py_file, unused_imports)
                is_has_diff = next(get_diff, None)
                for diff in get_diff:
                    print(diff)
                if is_has_diff:
                    overwrite_permission = input(
                        f"Apply suggested changes to '{py_file}' [y/n/q] ? > "
                    )
                    if overwrite_permission == "y":
                        self.overwrite(py_file, unused_imports)
                    elif overwrite_permission == "q":
                        break
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

    def context_diff(self, file_path, unused_imports):
        with tokenize.open(file_path) as stream:
            old_sourcesource = stream.read()
        unused_imports = [
            unused_import["name"] for unused_import in unused_imports
        ]
        new_source = filter_unused_imports(
            source=old_sourcesource, unused_imports=unused_imports
        )
        return difflib.context_diff(
            old_sourcesource.splitlines(), new_source.splitlines()
        )


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
