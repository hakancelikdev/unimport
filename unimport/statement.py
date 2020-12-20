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


class ImportFrom(NamedTuple):
    lineno: int
    column: int
    name: str
    package: str
    star: bool
    suggestions: List[str]

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))


class Name(NamedTuple):
    lineno: int
    name: str
    is_all: bool = False

    @property
    def is_attribute(self):
        return "." in self.name

    def match(self, imp: Union[Import, ImportFrom]) -> bool:
        if self.is_attribute:
            return self.__attribute_match(imp)
        else:
            return self.__name_match(imp)

    def __attribute_match(self, imp: Union[Import, ImportFrom]) -> bool:
        """if the name is a attribute."""
        match = ".".join(self.name.split(".")[: len(imp)]) == imp.name
        return imp.lineno < self.lineno and match

    def __name_match(self, imp: Union[Import, ImportFrom]) -> bool:
        """if the name is a normal name."""
        match = self.name == imp.name
        if self.is_all:
            return match
        else:
            return imp.lineno < self.lineno and match
