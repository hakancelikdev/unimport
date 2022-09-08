from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [Name(lineno=3, name="ImportError", is_all=False)]
IMPORTS: List[Union[Import, ImportFrom]] = [Import(lineno=7, column=1, name="t", package="t")]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [Import(lineno=7, column=1, name="t", package="t")]
