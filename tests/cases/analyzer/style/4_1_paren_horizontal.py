from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="y", is_all=False),
    Name(lineno=6, name="q", is_all=False),
    Name(lineno=6, name="e", is_all=False),
    Name(lineno=6, name="r", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="q", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="e", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=3, name="r", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=4, name="t", package="x", star=False, suggestions=[]),
    Import(lineno=2, column=1, name="y", package="y"),
    Import(lineno=3, column=1, name="u", package="u"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=3, column=1, name="u", package="u"),
    ImportFrom(lineno=1, column=4, name="t", package="x", star=False, suggestions=[]),
]
