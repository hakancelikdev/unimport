from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=9, name="ValueError", is_all=False),
    Name(lineno=9, name="TypeError", is_all=False),
    Name(lineno=14, name="ValueError", is_all=False),
    Name(lineno=14, name="TypeError", is_all=False),
    Name(lineno=14, name="KeyError", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=5, column=1, name="os", package="os"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=5, column=1, name="os", package="os"),
]
