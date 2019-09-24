import os
import re

from unimport import config

IGNORE = [i for i in config.CONFIG["ignore"]]
try:
    EXTRA_IGNORE = [i for i in config.CONFIG["extra_ignore"]]
    IGNORE = set(IGNORE + EXTRA_IGNORE)
except KeyError:
    pass
IGNORE_FILES = re.compile("|".join(IGNORE))


def in_blacklist(file):
    return IGNORE_FILES.match(file) != None


def get_files(direction):
    for root, dirs, files in os.walk(direction):
        if in_blacklist(root):
            continue
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith(".py") and not file_path.endswith("__init__.py"):
                yield file_path
