from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="y", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=2, name="z", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=3, name="t", package="x", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="t", package="t"),
    ImportFrom(
        lineno=3, column=1, name="t", package="l", star=False, suggestions=[]
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=3, column=1, name="t", package="l", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="t", package="t"),
    ImportFrom(
        lineno=1, column=3, name="t", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=2, name="z", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=1, name="y", package="x", star=False, suggestions=[]
    ),
]
