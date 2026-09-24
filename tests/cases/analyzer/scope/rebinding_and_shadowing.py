from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=2, name="b1", is_all=False),
    Name(lineno=3, name="print", is_all=False),
    Name(lineno=3, name="b1", is_all=False),
    Name(lineno=7, name="b2", is_all=False),
    Name(lineno=8, name="b2", is_all=False),
    Name(lineno=12, name="b3", is_all=False),
    Name(lineno=17, name="b4", is_all=False),
    Name(lineno=18, name="g", is_all=False),
    Name(lineno=22, name="b5", is_all=False),
    Name(lineno=23, name="print", is_all=False),
    Name(lineno=23, name="b5", is_all=False),
    Name(lineno=28, name="b6", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="b1", package="b1"),
    Import(lineno=5, column=1, name="b2", package="b2"),
    Import(lineno=10, column=1, name="b3", package="b3"),
    Import(lineno=14, column=1, name="b4", package="b4"),
    Import(lineno=20, column=1, name="b5", package="b5"),
    Import(lineno=25, column=1, name="b6", package="b6"),
    Import(lineno=27, column=1, name="b6", package="b6"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=25, column=1, name="b6", package="b6"),
    Import(lineno=20, column=1, name="b5", package="b5"),
    Import(lineno=14, column=1, name="b4", package="b4"),
    Import(lineno=10, column=1, name="b3", package="b3"),
    Import(lineno=5, column=1, name="b2", package="b2"),
    Import(lineno=1, column=1, name="b1", package="b1"),
]
