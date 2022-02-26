from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="y", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=2, column=1, name="y", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=3, column=1, name="x", package="t", star=False, suggestions=[]
    ),
    Import(lineno=4, column=1, name="re", package="re"),
    Import(lineno=5, column=1, name="ll", package="ll"),
    Import(lineno=6, column=1, name="ll", package="ll"),
    ImportFrom(
        lineno=7, column=1, name="e", package="c", star=False, suggestions=[]
    ),
    Import(lineno=8, column=1, name="e", package="e"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=8, column=1, name="e", package="e"),
    ImportFrom(
        lineno=7, column=1, name="e", package="c", star=False, suggestions=[]
    ),
    Import(lineno=6, column=1, name="ll", package="ll"),
    Import(lineno=5, column=1, name="ll", package="ll"),
    Import(lineno=4, column=1, name="re", package="re"),
    ImportFrom(
        lineno=3, column=1, name="x", package="t", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=2, column=1, name="y", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=1, name="y", package="x", star=False, suggestions=[]
    ),
]
