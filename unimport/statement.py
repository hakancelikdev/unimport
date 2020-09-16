from typing import List, NamedTuple


class Name(NamedTuple):
    lineno: int
    name: str


class Import(Name):
    lineno: int
    name: str


class ImportFrom(NamedTuple):
    lineno: int
    name: str
    star: bool
    suggestion: List[str]
