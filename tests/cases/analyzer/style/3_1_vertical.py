from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=11, name="y", is_all=False),
    Name(lineno=11, name="q", is_all=False),
    Name(lineno=11, name="e", is_all=False),
    Name(lineno=11, name="r", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="q", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="e", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=3, name="r", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=4, name="t", package="x", star=False, suggestions=[]),
    Import(lineno=7, column=1, name="y", package="y"),
    Import(lineno=8, column=1, name="u", package="u"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=8, column=1, name="u", package="u"),
    ImportFrom(lineno=1, column=4, name="t", package="x", star=False, suggestions=[]),
]
