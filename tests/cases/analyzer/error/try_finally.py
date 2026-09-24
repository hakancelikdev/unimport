from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=12, name="ImportError", is_all=False),
    Name(lineno=15, name="print", is_all=False),
    Name(lineno=15, name="json", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=2, column=1, name="os", package="os"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=2, column=1, name="os", package="os"),
]
