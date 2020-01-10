import os
import pathlib
import re
import tokenize

from unimport.unused import filter_unused_imports


def get_files(src, config):
    ignored_folders = re.compile("|".join(set(config.ignored_folders)))
    ignored_files = re.compile("|".join(set(config.ignored_files)))

    def _is_ignored_folder(path):
        return ignored_folders.match(path) is not None

    def _is_ignored_file(path):
        return (
            not path.endswith(".py") or ignored_files.match(path) is not None
        )

    if src.is_dir():
        for root, dirs, files in os.walk(src):
            if _is_ignored_folder(root):
                continue

            for name in files:
                file_path = os.path.join(root, name)
                if not _is_ignored_file(file_path):
                    yield file_path

    elif not _is_ignored_file(src.name):
        yield str(src)


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
