from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = []
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
