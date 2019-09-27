import os

from unimport.config import is_ignore_files, is_ignore_folder


def get_files(direction):
    for root, dirs, files in os.walk(direction):
        if is_ignore_folder(root):
            continue
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith(".py") and not is_ignore_files(file_path):
                yield file_path
