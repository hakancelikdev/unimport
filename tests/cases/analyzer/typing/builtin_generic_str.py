from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="x", is_all=False),
    Name(lineno=4, name="list", is_all=False),
    Name(lineno=4, name="Bar", is_all=False),
    Name(lineno=7, name="dict", is_all=False),
    Name(lineno=7, name="str", is_all=False),
    Name(lineno=7, name="Baz", is_all=False),
    Name(lineno=7, name="tuple", is_all=False),
    Name(lineno=7, name="Qux", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="Bar", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="Baz", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=3, name="Qux", package="foo", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
