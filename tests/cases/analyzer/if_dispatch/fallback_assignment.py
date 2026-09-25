from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="sys.version_info", is_all=False),
    Name(lineno=6, name="tomllib", is_all=False),
    Name(lineno=8, name="sys.platform", is_all=False),
    Name(lineno=10, name="sys.platform", is_all=False),
    Name(lineno=13, name="winreg", is_all=False),
    Name(lineno=13, name="object", is_all=False),
    Name(lineno=15, name="sys.version_info", is_all=False),
    Name(lineno=16, name="Missing", is_all=False),
    Name(lineno=20, name="sys.version_info", is_all=False),
    Name(lineno=23, name="other", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="sys", package="sys"),
    Import(lineno=21, column=1, name="json", package="json"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=21, column=1, name="json", package="json"),
]
