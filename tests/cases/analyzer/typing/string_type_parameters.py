from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=8, name="Money", is_all=False),
    Name(lineno=8, name="Decimal", is_all=False),
    Name(lineno=11, name="T", is_all=False),
    Name(lineno=12, name="value", is_all=False),
    Name(lineno=11, name="T", is_all=False),
    Name(lineno=11, name="Fraction", is_all=False),
    Name(lineno=11, name="Number", is_all=False),
    Name(lineno=15, name="Protocol", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=3, column=1, name="Decimal", package="decimal", star=False, suggestions=[]),
    ImportFrom(lineno=4, column=1, name="Fraction", package="fractions", star=False, suggestions=[]),
    ImportFrom(lineno=5, column=1, name="Number", package="numbers", star=False, suggestions=[]),
    ImportFrom(lineno=6, column=1, name="Protocol", package="typing", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
