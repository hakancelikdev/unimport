from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=12, name="p", is_all=False),
    Name(lineno=12, name="Path", is_all=False),
    Name(lineno=13, name="print", is_all=False),
    Name(lineno=13, name="ll", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=1, name="x", package="t", star=False, suggestions=[]),
    Import(lineno=4, column=1, name="re", package="re"),
    Import(lineno=5, column=1, name="ll", package="ll"),
    Import(lineno=6, column=1, name="ll", package="ll"),
    ImportFrom(lineno=7, column=1, name="e", package="c", star=False, suggestions=[]),
    Import(lineno=8, column=1, name="e", package="e"),
    ImportFrom(
        lineno=9,
        column=1,
        name="Path",
        package="pathlib",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=10,
        column=1,
        name="Path",
        package="pathlib",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=9,
        column=1,
        name="Path",
        package="pathlib",
        star=False,
        suggestions=[],
    ),
    Import(lineno=8, column=1, name="e", package="e"),
    ImportFrom(lineno=7, column=1, name="e", package="c", star=False, suggestions=[]),
    Import(lineno=5, column=1, name="ll", package="ll"),
    Import(lineno=4, column=1, name="re", package="re"),
    ImportFrom(lineno=3, column=1, name="x", package="t", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="y", package="x", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=1, name="y", package="x", star=False, suggestions=[]),
]
