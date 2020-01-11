import os
import pathlib
import re
import tokenize

from unimport.unused import filter_unused_imports


def get_files(src, config):
    p = pathlib.Path(src)

    def _is_ignored(path):
        for ignore_rule in config.ignore:
            for i in p.glob(ignore_rule):
                if str(path).startswith(str(i)):
                    return True

    for file in p.glob("**/*.py"):
        if not _is_ignored(file):
            yield file


def overwrite(file_path, unused_imports):
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
