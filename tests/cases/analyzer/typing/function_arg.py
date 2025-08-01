from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="List", is_all=False),
    Name(lineno=4, name="Dict", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="Dict",
        package="typing",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=1,
        column=2,
        name="List",
        package="typing",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
