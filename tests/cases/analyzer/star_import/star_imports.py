from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=9, name="print", is_all=False),
    Name(lineno=9, name="match", is_all=False),
    Name(lineno=10, name="print", is_all=False),
    Name(lineno=10, name="search", is_all=False),
    Name(lineno=11, name="print", is_all=False),
    Name(lineno=11, name="NAME", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1, column=1, name="os", package="os", star=True, suggestions=[]
    ),
    ImportFrom(
        lineno=2, column=1, name="y", package="x", star=False, suggestions=[]
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
        name="lib2to3.pgen2.token",
        package="lib2to3.pgen2.token",
        star=True,
        suggestions=["NAME"],
    ),
    ImportFrom(
        lineno=6,
        column=1,
        name="lib2to3.fixer_util",
        package="lib2to3.fixer_util",
        star=True,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=6,
        column=1,
        name="lib2to3.fixer_util",
        package="lib2to3.fixer_util",
        star=True,
        suggestions=[],
    ),
    ImportFrom(
        lineno=5,
        column=1,
        name="lib2to3.pgen2.token",
        package="lib2to3.pgen2.token",
        star=True,
        suggestions=["NAME"],
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
        lineno=2, column=1, name="y", package="x", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=1, column=1, name="os", package="os", star=True, suggestions=[]
    ),
]
