import os
import sys
import tokenize

from unimport.files import get_files
from unimport.unused import get_unused


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
    try:
        source_file_or_directory = sys.argv[1]
    except IndexError:
        source_file_or_directory = "."
    if os.path.isdir(source_file_or_directory):
        # folder
        for file in get_files(source_file_or_directory):
            for un_used in get_unused_imports(file):
                print(un_used)
    else:
        # file
        file_path = os.path.join(os.getcwd(), source_file_or_directory)
        if file_path.endswith(".py"):
            for un_used in get_unused_imports(file_path):
                print(un_used)


if __name__ == "__main__":
    console_scripts()
