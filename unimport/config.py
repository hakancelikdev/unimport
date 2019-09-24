import configparser
import pathlib
import os

CONFIG = configparser.ConfigParser(allow_no_value=True)
BUILTIN_CONFIG = pathlib.Path(__file__).parent / ".unimport.cfg"
CONFIG.read(BUILTIN_CONFIG)

EXTRA_CONFIG = str(pathlib.Path().cwd()) + os.sep + ".unimport.cfg"
if os.path.exists(EXTRA_CONFIG):
    CONFIG.read(EXTRA_CONFIG)
