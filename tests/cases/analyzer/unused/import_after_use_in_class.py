from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=2, name="x", is_all=False),
    Name(lineno=2, name="sys.platform", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="sys", package="sys"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="sys", package="sys"),
]
