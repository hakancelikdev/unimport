from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="used", is_all=False),
    Name(lineno=6, name="helper", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name=".", package=".", star=True, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="helper", package="..", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=2, name="unused", package="..", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=1, name="used", package=".", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=1, name=".models", package=".models", star=True, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=2, name="unused", package="..", star=False, suggestions=[]),
]
