from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=9, name="print", is_all=False),
    Name(lineno=9, name="os", is_all=False),
    Name(lineno=10, name="print", is_all=False),
    Name(lineno=10, name="OrderedDict", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="os", package="os"),
    Import(lineno=4, column=1, name="sys", package="sys"),
    ImportFrom(
        lineno=7,
        column=1,
        name="OrderedDict",
        package="collections",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=4, column=1, name="sys", package="sys"),
]
