from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=5, name="time", is_all=False),
    Name(lineno=6, name="path.join", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="time",
        package="time",
        star=True,
        suggestions=["time"],
    ),
    ImportFrom(
        lineno=2,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=["path"],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=2,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=["path"],
    )
]
