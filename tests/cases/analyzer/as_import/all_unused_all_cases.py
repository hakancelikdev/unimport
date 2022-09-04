from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="z", package="x", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="x", package="x"),
    ImportFrom(
        lineno=3, column=1, name="ss", package="t", star=False, suggestions=[]
    ),
    Import(lineno=4, column=1, name="x", package="le"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="x", package="le"),
    ImportFrom(
        lineno=3, column=1, name="ss", package="t", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="x", package="x"),
    ImportFrom(
        lineno=1, column=1, name="z", package="x", star=False, suggestions=[]
    ),
]
