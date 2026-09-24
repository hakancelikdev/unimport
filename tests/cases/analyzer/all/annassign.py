from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="__all__", is_all=False),
    Name(lineno=3, name="list", is_all=False),
    Name(lineno=3, name="str", is_all=False),
    Name(lineno=3, name="A", is_all=True),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="A", package=".mod", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="B", package=".mod", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=2, name="B", package=".mod", star=False, suggestions=[]),
]
