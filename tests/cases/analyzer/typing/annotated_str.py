from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="x", is_all=False),
    Name(lineno=6, name="Annotated", is_all=False),
    Name(lineno=6, name="Bar", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="Annotated", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=1, name="Bar", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=2, name="doc", package="foo", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=3, column=2, name="doc", package="foo", star=False, suggestions=[]),
]
