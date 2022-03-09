from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=4, name="__future__.absolute_import", is_all=False)
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="__future__", package="__future__")
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
