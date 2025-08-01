from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="Exception", is_all=False),
    Name(lineno=8, name="BaseException", is_all=False),
    Name(lineno=13, name="OSError", is_all=False),
    Name(lineno=18, name="OSError", is_all=False),
    Name(lineno=18, name="AttributeError", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = []
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
