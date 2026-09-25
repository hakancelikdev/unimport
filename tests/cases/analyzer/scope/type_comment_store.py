from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="json", is_all=False),
    Name(lineno=3, name="json", is_all=False),
    Name(lineno=3, name="x", is_all=False),
    Name(lineno=4, name="print", is_all=False),
    Name(lineno=4, name="json", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="json", package="json"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
