from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=3, name="sys.version_info", is_all=False),
    Name(lineno=9, name="Literal", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [Import(lineno=1, column=1, name="sys", package="sys")]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
