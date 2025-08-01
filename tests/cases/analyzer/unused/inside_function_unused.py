from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="print", is_all=False),
    Name(lineno=6, name="t", is_all=False),
    Name(lineno=7, name="ImportError", is_all=False),
    Name(lineno=10, name="math.pi", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=2, name="z", package="x", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=2, name="z", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
]
