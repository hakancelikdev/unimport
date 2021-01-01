import operator
from typing import List, NamedTuple, Union

__all__ = ["Import", "ImportFrom", "Name"]


class Import(NamedTuple):
    lineno: int
    column: int
    name: str
    package: str

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))

    def is_match_sub_packages(self, name_name) -> bool:
        return self.name.split(".")[0] == name_name


class ImportFrom(NamedTuple):
    lineno: int
    column: int
    name: str
    package: str
    star: bool
    suggestions: List[str]

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))

    def is_match_sub_packages(self, name_name):
        return False


class Name(NamedTuple):
    lineno: int
    name: str
    is_all: bool = False

    @property
    def is_attribute(self):
        return "." in self.name

    def match(self, imp: Union[Import, ImportFrom]) -> bool:
        if self.is_all:
            return self.name == imp.name
        elif self.is_attribute:
            return imp.lineno < self.lineno and (
                ".".join(self.name.split(".")[: len(imp)]) == imp.name
                or imp.is_match_sub_packages(self.name)
            )
        else:
            return (imp.lineno < self.lineno) and (
                self.name == imp.name or imp.is_match_sub_packages(self.name)
            )
