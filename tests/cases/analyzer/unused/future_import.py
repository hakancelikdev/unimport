from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [Name(lineno=4, name="__future__.absolute_import", is_all=False)]
IMPORTS: list[Union[Import, ImportFrom]] = [Import(lineno=1, column=1, name="__future__", package="__future__")]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
