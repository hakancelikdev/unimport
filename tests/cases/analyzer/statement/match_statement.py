from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=3, name="sort_by", is_all=False),
    Name(lineno=4, name="sort_by", is_all=False),
    Name(lineno=5, name="sort_by", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = []
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
