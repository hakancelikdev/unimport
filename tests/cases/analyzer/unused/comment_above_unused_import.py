from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=6, name="print", is_all=False),
    Name(lineno=6, name="os", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="os", package="os"),
    ImportFrom(
        lineno=4,
        column=1,
        name="compile_command",
        package="codeop",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=4,
        column=1,
        name="compile_command",
        package="codeop",
        star=False,
        suggestions=[],
    )
]
