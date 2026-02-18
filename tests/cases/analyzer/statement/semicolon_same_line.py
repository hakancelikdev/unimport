from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=1, name="print", is_all=False),
    Name(lineno=1, name="pathlib.Path", is_all=False),
    Name(lineno=1, name="__file__", is_all=False),
    Name(lineno=2, name="sys.exit", is_all=False),
    Name(lineno=2, name="doctest.testmod", is_all=False),
    Name(lineno=2, name="doctest.ELLIPSIS", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="pathlib", package="pathlib"),
    Import(lineno=2, column=1, name="doctest", package="doctest"),
    Import(lineno=2, column=2, name="sys", package="sys"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
