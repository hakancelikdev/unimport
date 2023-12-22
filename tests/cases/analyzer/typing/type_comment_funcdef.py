from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=4, name="str", is_all=False),
    Name(lineno=4, name="List", is_all=False),
    Name(lineno=4, name="str", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="List",
        package="typing",
        star=False,
        suggestions=[],
    )
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
