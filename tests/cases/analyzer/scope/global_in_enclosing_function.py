from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=5, name="json", is_all=False),
    Name(lineno=11, name="json.dumps", is_all=False),
    Name(lineno=13, name="h", is_all=False),
    Name(lineno=15, name="g", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="json", package="json"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
