from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="CodeRange", is_all=False),
    Name(lineno=4, name="PositionProvider", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="libcst.metadata",
        package="libcst.metadata",
        star=True,
        suggestions=["CodeRange", "PositionProvider"],
    )
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="libcst.metadata",
        package="libcst.metadata",
        star=True,
        suggestions=["CodeRange", "PositionProvider"],
    )
]
