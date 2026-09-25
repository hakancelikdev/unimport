from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="T", is_all=False),
    Name(lineno=6, name="Decimal", is_all=False),
    Name(lineno=6, name="TypeVar", is_all=False),
    Name(lineno=7, name="P", is_all=False),
    Name(lineno=7, name="Fraction", is_all=False),
    Name(lineno=7, name="ParamSpec", is_all=False),
    Name(lineno=8, name="mode", is_all=False),
    Name(lineno=8, name="Literal", is_all=False),
    Name(lineno=9, name="amount", is_all=False),
    Name(lineno=9, name="Annotated", is_all=False),
    Name(lineno=9, name="int", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="Decimal", package="decimal", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=1, name="Fraction", package="fractions", star=False, suggestions=[]),
    ImportFrom(lineno=3, column=1, name="Number", package="numbers", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=1, name="Annotated", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=2, name="Literal", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=3, name="ParamSpec", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=4, name="TypeVar", package="typing", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=3, column=1, name="Number", package="numbers", star=False, suggestions=[]),
]
