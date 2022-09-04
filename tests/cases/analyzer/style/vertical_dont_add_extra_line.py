from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=7, name="test_list", is_all=False),
    Name(lineno=7, name="List", is_all=False),
    Name(lineno=7, name="str", is_all=False),
    Name(lineno=7, name="spam", is_all=False),
    Name(lineno=7, name="eggs", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="sys", package="sys"),
    ImportFrom(
        lineno=2,
        column=1,
        name="List",
        package="typing",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="sys", package="sys")
]
