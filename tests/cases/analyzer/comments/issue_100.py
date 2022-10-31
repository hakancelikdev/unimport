from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [
    Name(lineno=11, name="os", is_all=False),
    Name(lineno=11, name="Union", is_all=False),
    Name(lineno=11, name="driver", is_all=False),
    Name(lineno=11, name="Grammar", is_all=False),
]
IMPORTS: List[Union[Import, ImportFrom]] = [
    Import(lineno=2, column=1, name="os", package="os"),
    ImportFrom(lineno=4, column=1, name="Union", package="typing", star=False, suggestions=[]),
    ImportFrom(lineno=7, column=1, name="token", package=".pgen2", star=False, suggestions=[]),
    ImportFrom(lineno=8, column=1, name="driver", package=".pgen2", star=False, suggestions=[]),
    ImportFrom(lineno=10, column=1, name="Grammar", package=".pgen2.grammar", star=False, suggestions=[]),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(lineno=7, column=1, name="token", package=".pgen2", star=False, suggestions=[])
]
