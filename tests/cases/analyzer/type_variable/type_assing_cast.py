from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=3, name="TYPE_CHECKING", is_all=False),
    Name(lineno=7, name="HistoryType", is_all=False),
    Name(lineno=7, name="QtWebKit.QWebHistory", is_all=False),
    Name(lineno=7, name="cast", is_all=False),
    Name(lineno=7, name="return_value", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="TYPE_CHECKING",
        package="typing",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=4,
        column=1,
        name="QtWebKit",
        package="PyQt5",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
