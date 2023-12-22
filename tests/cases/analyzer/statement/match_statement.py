from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=5, name="sort_by", is_all=False),
    Name(lineno=6, name="sort_by", is_all=False),
    Name(lineno=7, name="sort_by", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = []
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
