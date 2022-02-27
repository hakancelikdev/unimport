from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=5, name="print", is_all=False),
    Name(lineno=5, name="datetime.datetime.now", is_all=False),
    Name(lineno=5, name="datetime.datetime", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="datetime", package="datetime"),
    ImportFrom(
        lineno=2,
        column=1,
        name="relativedelta",
        package="dateutil.relativedelta",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=2,
        column=1,
        name="relativedelta",
        package="dateutil.relativedelta",
        star=False,
        suggestions=[],
    )
]
