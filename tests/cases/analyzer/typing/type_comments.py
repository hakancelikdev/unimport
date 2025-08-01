from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="Any", is_all=False),
    Name(lineno=6, name="str", is_all=False),
    Name(lineno=6, name="Union", is_all=False),
    Name(lineno=6, name="Tuple", is_all=False),
    Name(lineno=6, name="Tuple", is_all=False),
    Name(lineno=6, name="str", is_all=False),
    Name(lineno=6, name="str", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="Any", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="Tuple", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=1, name="Union", package="typing", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
