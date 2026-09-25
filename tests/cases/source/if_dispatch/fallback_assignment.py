import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    tomllib = None

if sys.platform == "win32":
    import winreg
elif sys.platform == "darwin":
    from _osx_support import winreg
else:
    winreg: object = None

if sys.version_info >= (3, 12):
    Missing = None
else:
    from typing_extensions import Missing

if sys.version_info >= (3, 11):
    import json
else:
    other = None
