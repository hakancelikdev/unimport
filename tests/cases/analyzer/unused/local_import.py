from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=9, name="hakan", is_all=False),
    Name(lineno=10, name="b", is_all=False),
    Name(lineno=11, name="q", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="y", package=".x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=2, column=1, name="t", package="..z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=3,
        column=1,
        name="a",
        package="...t",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=4, column=1, name="y", package=".x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4,
        column=2,
        name="hakan",
        package=".x",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=5, column=1, name="u", package="..z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=5, column=2, name="b", package="..z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6,
        column=1,
        name="z",
        package="...t",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=6,
        column=2,
        name="q",
        package="...t",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=6,
        column=1,
        name="z",
        package="...t",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=5, column=1, name="u", package="..z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=1, name="y", package=".x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=3,
        column=1,
        name="a",
        package="...t",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=2, column=1, name="t", package="..z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=1, name="y", package=".x", star=False, suggestions=[]
    ),
]
