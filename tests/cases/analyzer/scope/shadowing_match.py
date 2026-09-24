from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=8, name="value", is_all=False),
    Name(lineno=10, name="os", is_all=False),
    Name(lineno=10, name="rest", is_all=False),
    Name(lineno=12, name="sys", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=3, column=1, name="os", package="os"),
    Import(lineno=4, column=1, name="sys", package="sys"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="sys", package="sys"),
    Import(lineno=3, column=1, name="os", package="os"),
]
