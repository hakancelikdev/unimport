from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = []
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="c", package="a.b"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="c", package="a.b"),
]
