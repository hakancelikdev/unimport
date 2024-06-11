from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=4, name="t.TYPE_CHECKING", is_all=False),
    Name(lineno=8, name="QtCore.QThread", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="QtCore", package="qtpy", star=False, suggestions=[]),
    Import(lineno=2, column=1, name="t", package="typing"),
    ImportFrom(lineno=5, column=1, name="QtCore", package="PySide6", star=False, suggestions=[]),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=2, column=1, name="t", package="typing"),
    ImportFrom(lineno=5, column=1, name="QtCore", package="PySide6", star=False, suggestions=[]),
]
