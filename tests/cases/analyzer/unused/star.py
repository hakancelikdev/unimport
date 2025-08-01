from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [Name(lineno=4, name="walk", is_all=False)]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=["walk"],
    )
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=["walk"],
    )
]
