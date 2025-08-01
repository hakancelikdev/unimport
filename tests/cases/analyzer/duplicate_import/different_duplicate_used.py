from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="print", is_all=False),
    Name(lineno=4, name="z", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="z", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="z", package="y", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="z", package="x", star=False, suggestions=[])
]
