from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=1, name="condition", is_all=False),
    Name(lineno=3, name="condition_2", is_all=False),
    Name(lineno=8, name="ii", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=2, name="ii", package="x", star=False, suggestions=[]),
    Import(lineno=4, column=2, name="tt", package="x"),
    Import(lineno=6, column=1, name="yy", package="y"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=6, column=1, name="yy", package="y"),
    Import(lineno=4, column=2, name="tt", package="x"),
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
]
