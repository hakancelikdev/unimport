from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="sys.version_info", is_all=False),
    Name(lineno=5, name="TYPE_CHECKING", is_all=False),
    Name(lineno=8, name="Any", is_all=False),
    Name(lineno=11, name="Any", is_all=False),
    Name(lineno=11, name="Any", is_all=False),
    Name(lineno=11, name="Any", is_all=False),
    Name(lineno=19, name="print", is_all=False),
    Name(lineno=19, name="ForwardRef", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="sys", package="sys"),
    ImportFrom(lineno=2, column=1, name="TYPE_CHECKING", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=2, name="Any", package="typing", star=False, suggestions=[]),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = []
