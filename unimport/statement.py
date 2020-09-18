from typing import List, NamedTuple


class Name(NamedTuple):
    lineno: int
    name: str


class Import(Name):
    pass


class ImportFrom(NamedTuple):
    lineno: int
    name: str
    star: bool
    suggestions: List[str]
