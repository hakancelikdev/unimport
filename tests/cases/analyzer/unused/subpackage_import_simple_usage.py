from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="print", is_all=False),
    Name(lineno=3, name="os.getcwd", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="os.path", package="os.path"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
