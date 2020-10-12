import operator
from typing import List, NamedTuple, Optional, Union


class Import(NamedTuple):
    lineno: int
    column: int
    name: str
    module_name: Optional[str] = None

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))


class ImportFrom(NamedTuple):
    lineno: int
    column: int
    name: str
    star: bool
    suggestions: List[str]
    module_name: Optional[str] = None

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))


class Name(NamedTuple):
    lineno: int
    name: str

    def match(self, imp: Union[Import, ImportFrom]) -> bool:
        return (
            imp.lineno < self.lineno
            and ".".join(self.name.split(".")[: len(imp)]) == imp.name
        )
