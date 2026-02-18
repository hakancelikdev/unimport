from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=1, name="print", is_all=False),
    Name(lineno=1, name="sys.path", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=3, column=1, name="sys", package="sys"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=3, column=1, name="sys", package="sys"),
]
