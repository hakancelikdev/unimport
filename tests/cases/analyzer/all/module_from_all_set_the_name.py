from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="__all__", is_all=False),
    Name(lineno=8, name="Any", is_all=False),
    Name(lineno=4, name="Test", is_all=True),
    Name(lineno=5, name="Test2", is_all=True),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="typing", package="typing", star=True, suggestions=["Any"]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="typing", package="typing", star=True, suggestions=["Any"]),
]
