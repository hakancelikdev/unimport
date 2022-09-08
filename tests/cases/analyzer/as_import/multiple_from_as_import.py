from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = []
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=1, column=1, name="c", package="f", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="k", package="f", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=3, name="ii", package="f", star=False, suggestions=[]),
    ImportFrom(
        lineno=2,
        column=1,
        name="bar",
        package="fo",
        star=False,
        suggestions=[],
    ),
    ImportFrom(lineno=2, column=2, name="i", package="fo", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=3, name="z", package="fo", star=False, suggestions=[]),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=2, column=3, name="z", package="fo", star=False, suggestions=[]),
    ImportFrom(lineno=2, column=2, name="i", package="fo", star=False, suggestions=[]),
    ImportFrom(
        lineno=2,
        column=1,
        name="bar",
        package="fo",
        star=False,
        suggestions=[],
    ),
    ImportFrom(lineno=1, column=3, name="ii", package="f", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=2, name="k", package="f", star=False, suggestions=[]),
    ImportFrom(lineno=1, column=1, name="c", package="f", star=False, suggestions=[]),
]
