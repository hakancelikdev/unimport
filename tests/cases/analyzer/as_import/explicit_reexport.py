from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = []
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=2, column=1, name="path", package="os.path"),
    ImportFrom(lineno=3, column=2, name="Q", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=3, name="Unused", package="foo", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=3, column=3, name="Unused", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=2, name="Q", package="foo", star=False, suggestions=[]),
    Import(lineno=2, column=1, name="path", package="os.path"),
]
