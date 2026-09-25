from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="config", is_all=False),
    Name(lineno=3, name="load", is_all=False),
    Name(lineno=4, name="config", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="config", package="config"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
