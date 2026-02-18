from typing import Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: list[Name] = [
    Name(lineno=4, name="urllib.parse.urlparse", is_all=False),
    Name(lineno=4, name="urllib.parse", is_all=False),
]
IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="urllib.request", package="urllib.request"),
    Import(lineno=2, column=1, name="urllib.parse", package="urllib.parse"),
]
UNUSED_IMPORTS: list[Union[Import, ImportFrom]] = [
    Import(lineno=1, column=1, name="urllib.request", package="urllib.request"),
]
