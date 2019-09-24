import os
import sys
import tokenize

from unimport import files, unused


def get_unused_imports(file_path):
    try:
        source = tokenize.open(file_path).read()
    except OSError:
        pass
    else:
        unused_imports = unused.get_unused(source=source)
        for imports in unused_imports:
            imports.update(path=file_path.replace(os.getcwd(), ""))
            yield imports


def console_scripts():
    try:
        source_file_or_directory = sys.argv[1]
    except IndexError:
        source_file_or_directory = "."
    if os.path.isdir(source_file_or_directory):
        # folder
        for file in files.get_files(source_file_or_directory):
            for un_used in get_unused_imports(file):
                print(un_used)
    else:
        # file
        file_path = os.path.join(os.getcwd(), source_file_or_directory)
        if file_path.endswith(".py"):
            for un_used in get_unused_imports(file_path):
                print(un_used)
