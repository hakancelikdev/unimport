from types import ModuleType
from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    lineno: int
    name: str


class Import(NamedTuple):
    lineno: int
    name: str
    module: Optional[ModuleType]


class ImportFrom(NamedTuple):
    lineno: int
    name: str
    star: bool
    module: Optional[ModuleType]
    modules: List[str]
