from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=1, name="condition", is_all=False),
    Name(lineno=6, name="ii", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
    Import(lineno=4, column=1, name="yy", package="y"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="yy", package="y"),
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
]
