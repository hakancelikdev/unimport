from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=3, name="print", is_all=False),
    Name(lineno=3, name="t", is_all=False),
    Name(lineno=9, name="t", is_all=False),
    Name(lineno=12, name="f", is_all=False),
    Name(lineno=16, name="print", is_all=False),
    Name(lineno=16, name="t", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="t", package="t"),
    ImportFrom(lineno=6, column=1, name="t", package="l", star=False, suggestions=[]),
    ImportFrom(lineno=7, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=7, column=2, name="z", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=7, column=3, name="t", package="x", star=False, suggestions=[]),
    Import(lineno=10, column=1, name="x", package="x"),
    ImportFrom(lineno=14, column=1, name="ii", package="i", star=False, suggestions=[]),
    ImportFrom(lineno=14, column=2, name="t", package="i", star=False, suggestions=[]),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=14, column=1, name="ii", package="i", star=False, suggestions=[]),
    Import(lineno=10, column=1, name="x", package="x"),
    ImportFrom(lineno=7, column=2, name="z", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=7, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=6, column=1, name="t", package="l", star=False, suggestions=[]),
]
