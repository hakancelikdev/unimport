from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=7, name="print", is_all=False),
    Name(lineno=7, name="x", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="z", package="x", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="x", package="x"),
    ImportFrom(
        lineno=3, column=1, name="ss", package="t", star=False, suggestions=[]
    ),
    Import(lineno=4, column=1, name="bar", package="bar"),
    Import(lineno=4, column=2, name="i", package="i"),
    Import(lineno=4, column=3, name="z", package="x"),
    Import(lineno=5, column=1, name="x", package="le"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=3, name="z", package="x"),
    Import(lineno=4, column=2, name="i", package="i"),
    Import(lineno=4, column=1, name="bar", package="bar"),
    ImportFrom(
        lineno=3, column=1, name="ss", package="t", star=False, suggestions=[]
    ),
    Import(lineno=2, column=1, name="x", package="x"),
    ImportFrom(
        lineno=1, column=1, name="z", package="x", star=False, suggestions=[]
    ),
]
