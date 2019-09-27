import configparser
import os
import pathlib
import re
import sys

CONFIG = configparser.ConfigParser(allow_no_value=True)
BUILTIN_CONFIG = pathlib.Path(__file__).parent / ".unimport.cfg"
try:
    directory = os.sep + sys.argv[1] + os.sep
except IndexError:
    directory = os.sep
EXTRA_CONFIG = str(pathlib.Path().cwd()) + directory + ".unimport.cfg"
if os.path.exists(EXTRA_CONFIG):
    CONFIG.read(EXTRA_CONFIG)
CONFIG.read(BUILTIN_CONFIG)

IGNORE_FOLDERS = re.compile("|".join(set([i for i in CONFIG["folders"]])))
IGNORE_FILES = re.compile("|".join(set([i for i in CONFIG["files"]])))


def is_ignore_folder(path):
    return IGNORE_FOLDERS.match(path) != None


def is_ignore_files(path):
    return IGNORE_FILES.match(path) != None
