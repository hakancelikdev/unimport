from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=5, name="print", is_all=False),
    Name(lineno=5, name="bar", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="c", package="a"),
    Import(lineno=1, column=2, name="k", package="l"),
    Import(lineno=1, column=3, name="ii", package="i"),
    Import(lineno=2, column=1, name="bar", package="bar"),
    Import(lineno=2, column=2, name="i", package="i"),
    Import(lineno=2, column=3, name="z", package="x"),
    Import(lineno=3, column=1, name="bar", package="bar"),
    Import(lineno=3, column=2, name="i", package="i"),
    Import(lineno=3, column=3, name="z", package="x"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=3, column=3, name="z", package="x"),
    Import(lineno=3, column=2, name="i", package="i"),
    Import(lineno=2, column=3, name="z", package="x"),
    Import(lineno=2, column=2, name="i", package="i"),
    Import(lineno=2, column=1, name="bar", package="bar"),
    Import(lineno=1, column=3, name="ii", package="i"),
    Import(lineno=1, column=2, name="k", package="l"),
    Import(lineno=1, column=1, name="c", package="a"),
]
