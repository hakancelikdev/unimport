from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=7, name="Alias", is_all=False),
    Name(lineno=7, name="TypeAlias", is_all=False),
    Name(lineno=7, name="Bar", is_all=False),
    Name(lineno=8, name="Other", is_all=False),
    Name(lineno=8, name="typing.TypeAlias", is_all=False),
    Name(lineno=8, name="list", is_all=False),
    Name(lineno=8, name="Baz", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="typing", package="typing"),
    ImportFrom(lineno=2, column=1, name="TypeAlias", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=1, name="Bar", package="foo", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=2, name="Baz", package="foo", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
