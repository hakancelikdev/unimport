from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=18, name="x", is_all=False),
    Name(lineno=18, name="e", is_all=False),
    Name(lineno=18, name="u", is_all=False),
    Name(lineno=18, name="c", is_all=False),
    Name(lineno=18, name="ff", is_all=False),
    Name(lineno=18, name="tt", is_all=False),
    Name(lineno=18, name="ll", is_all=False),
    Name(lineno=18, name="el", is_all=False),
    Name(lineno=18, name="tl", is_all=False),
    Name(lineno=18, name="si", is_all=False),
    Name(lineno=18, name="ug", is_all=False),
    Name(lineno=18, name="yt", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="x", package="x"),
    Import(lineno=1, column=2, name="x", package="x"),
    Import(lineno=1, column=3, name="yt", package="yt"),
    Import(lineno=2, column=1, name="e", package="e"),
    Import(lineno=2, column=2, name="y", package="y"),
    Import(lineno=2, column=3, name="e", package="e"),
    ImportFrom(
        lineno=3, column=1, name="u", package="z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=3, column=2, name="u", package="z", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=1, name="c", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=2, name="d", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=3, name="c", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=4, name="c", package="bb", star=False, suggestions=[]
    ),
    Import(lineno=5, column=1, name="ff", package="ff"),
    Import(lineno=5, column=2, name="tt", package="tt"),
    Import(lineno=5, column=3, name="ff", package="ff"),
    Import(lineno=5, column=4, name="ff", package="ff"),
    Import(lineno=5, column=5, name="tt", package="tt"),
    ImportFrom(
        lineno=6, column=1, name="ll", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=2, name="el", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=3, name="ll", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=4, name="el", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=5, name="tl", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=6, name="tl", package="ee", star=False, suggestions=[]
    ),
    Import(lineno=14, column=1, name="si", package="iss"),
    Import(lineno=14, column=2, name="si", package="si"),
    ImportFrom(
        lineno=15,
        column=1,
        name="ug",
        package="gu",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=15,
        column=2,
        name="ug",
        package="gu",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=15,
        column=1,
        name="ug",
        package="gu",
        star=False,
        suggestions=[],
    ),
    Import(lineno=14, column=1, name="si", package="iss"),
    ImportFrom(
        lineno=6, column=5, name="tl", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=2, name="el", package="ee", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=6, column=1, name="ll", package="ee", star=False, suggestions=[]
    ),
    Import(lineno=5, column=3, name="ff", package="ff"),
    Import(lineno=5, column=2, name="tt", package="tt"),
    Import(lineno=5, column=1, name="ff", package="ff"),
    ImportFrom(
        lineno=4, column=3, name="c", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=2, name="d", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=4, column=1, name="c", package="bb", star=False, suggestions=[]
    ),
    ImportFrom(
        lineno=3, column=1, name="u", package="z", star=False, suggestions=[]
    ),
    Import(lineno=2, column=2, name="y", package="y"),
    Import(lineno=2, column=1, name="e", package="e"),
    Import(lineno=1, column=1, name="x", package="x"),
]
