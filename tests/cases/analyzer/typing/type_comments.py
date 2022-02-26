from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=8, name="Any", is_all=False),
    Name(lineno=8, name="str", is_all=False),
    Name(lineno=8, name="Union", is_all=False),
    Name(lineno=8, name="Tuple", is_all=False),
    Name(lineno=8, name="Tuple", is_all=False),
    Name(lineno=8, name="str", is_all=False),
    Name(lineno=8, name="str", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=3,
        column=1,
        name="Any",
        package="typing",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=4,
        column=1,
        name="Tuple",
        package="typing",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=5,
        column=1,
        name="Union",
        package="typing",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = []
