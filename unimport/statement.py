import operator
from typing import List, NamedTuple, Union


class Import(NamedTuple):
    lineno: int
    column: int
    name: str

    def __len__(self):
        return operator.length_hint(self.name.split("."))


class ImportFrom(NamedTuple):
    lineno: int
    column: int
    name: str
    star: bool
    suggestions: List[str]

    def __len__(self):
        return operator.length_hint(self.name.split("."))


class Name(NamedTuple):
    lineno: int
    name: str

    def match(self, imp: Union[Import, ImportFrom]):
        if imp.lineno < self.lineno:
            return ".".join(self.name.split(".")[: len(imp)]) == imp.name
        return False
