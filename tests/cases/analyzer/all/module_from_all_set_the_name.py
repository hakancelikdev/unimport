from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=3, name="__all__", is_all=False),
    Name(lineno=8, name="Any", is_all=False),
    Name(lineno=4, name="Test", is_all=True),
    Name(lineno=5, name="Test2", is_all=True),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="typing", package="typing", star=True, suggestions=["Any"]),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="typing", package="typing", star=True, suggestions=["Any"]),
]
