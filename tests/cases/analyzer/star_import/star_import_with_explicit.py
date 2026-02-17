from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="print", is_all=False),
    Name(lineno=4, name="defaultdict", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="_collections",
        package="_collections",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=2,
        column=1,
        name="defaultdict",
        package="collections",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="_collections",
        package="_collections",
        star=True,
        suggestions=[],
    ),
]
