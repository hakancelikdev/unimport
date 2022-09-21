from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=3, name="sys.version_info", is_all=False),
    Name(lineno=9, name="Literal", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [Import(lineno=1, column=1, name="sys", package="sys")]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
