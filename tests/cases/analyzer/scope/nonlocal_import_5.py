from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [Name(lineno=5, name="x", is_all=False)]
IMPORTS: list[Union[Import, ImportFrom]] = [Import(lineno=1, column=1, name="x", package="x")]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
