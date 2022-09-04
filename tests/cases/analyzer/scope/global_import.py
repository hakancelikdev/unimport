from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [Name(lineno=6, name="x", is_all=False)]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="x", package="x"),
    Import(lineno=4, column=1, name="x", package="x"),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [Import(lineno=1, column=1, name="x", package="x")]
