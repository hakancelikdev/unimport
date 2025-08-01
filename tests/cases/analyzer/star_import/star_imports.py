from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=9, name="print", is_all=False),
    Name(lineno=9, name="match", is_all=False),
    Name(lineno=10, name="print", is_all=False),
    Name(lineno=10, name="search", is_all=False),
    Name(lineno=11, name="print", is_all=False),
    Name(lineno=11, name="AST", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=2,
        column=1,
        name="y",
        package="x",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=3,
        column=1,
        name="re",
        package="re",
        star=True,
        suggestions=["match", "search"],
    ),
    ImportFrom(
        lineno=4,
        column=1,
        name="t.s.d",
        package="t.s.d",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=5,
        column=1,
        name="ast",
        package="ast",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=6,
        column=1,
        name="AST",
        package="ast",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=5,
        column=1,
        name="ast",
        package="ast",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=4,
        column=1,
        name="t.s.d",
        package="t.s.d",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=3,
        column=1,
        name="re",
        package="re",
        star=True,
        suggestions=["match", "search"],
    ),
    ImportFrom(
        lineno=2,
        column=1,
        name="y",
        package="x",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=1,
        column=1,
        name="os",
        package="os",
        star=True,
        suggestions=[],
    ),
]
