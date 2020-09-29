from typing import List, NamedTuple


class Name(NamedTuple):
    lineno: int
    name: str


class Import(NamedTuple):
    lineno: int
    column: int
    name: str


class ImportFrom(NamedTuple):
    lineno: int
    column: int
    name: str
    star: bool
    suggestions: List[str]
