from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="total", is_all=False),
    Name(lineno=3, name="len", is_all=False),
    Name(lineno=3, name="sep", is_all=False),
    Name(lineno=3, name="items", is_all=False),
    Name(lineno=4, name="total", is_all=False),
    Name(lineno=4, name="sep", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=1, name="sep", package="os", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
