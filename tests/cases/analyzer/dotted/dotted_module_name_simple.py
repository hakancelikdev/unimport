from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="a.b", package="a.b"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="a.b", package="a.b"),
]
