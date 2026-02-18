from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = []
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="TYPE_CHECKING",
        package="typing",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=4,
        column=1,
        name="QtWebKit",
        package="PyQt5",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=4,
        column=1,
        name="QtWebKit",
        package="PyQt5",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=1,
        column=1,
        name="TYPE_CHECKING",
        package="typing",
        star=False,
        suggestions=[],
    ),
]
