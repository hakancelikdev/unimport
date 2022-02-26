import ast
import operator
import sys
from dataclasses import dataclass, field
from typing import ClassVar, Iterator, List, Set, Union

if sys.version_info >= (3, 8):
    from typing import Literal  # unimport: skip
else:
    from typing_extensions import Literal


__all__ = ("Import", "ImportFrom", "Name", "Scope")


@dataclass
class Import:
    imports: ClassVar[List[Union["Import", "ImportFrom"]]] = []

    lineno: int
    column: int
    name: str
    package: str

    node: ast.AST = field(init=False, repr=False, compare=False)

    def __len__(self) -> int:
        return operator.length_hint(self.name.split("."))

    def is_match_sub_packages(self, name_name) -> bool:
        return self.name.split(".")[0] == name_name

    @property
    def scope(self):
        return Scope.get_scope_by_current_node(self)

    def is_used(self) -> bool:
        for name in self.scope.names:
            if name is None:
                continue

            if name.match_import:
                if name.match_import == self:
                    return True
            elif name.match(self):
                return True

        return False

    def match_nearest_duplicate_import(self, name: "Name") -> bool:
        nearest_import = None

        scope = name.scope
        while scope:
            imports = [
                _import
                for _import in scope.imports
                if name.match_2(_import) and name.lineno > _import.lineno
            ]
            scope = scope.parent

            if imports:
                nearest_import = max(
                    filter(
                        lambda _import: _import.lineno
                        == max(
                            imports, key=lambda _import: _import.lineno
                        ).lineno,
                        imports,
                    ),
                    key=lambda _import: _import.column,
                )

            if nearest_import == self:
                return True

        return False

    @property
    def is_duplicate(self) -> bool:
        return [_import.name for _import in self.imports].count(self.name) > 1

    @classmethod
    def get_unused_imports(
        cls, include_star_import: bool = False
    ) -> Iterator[Union["Import", "ImportFrom"]]:
        for imp in reversed(Import.imports):
            if (
                include_star_import
                and isinstance(imp, ImportFrom)
                and imp.star
            ):
                yield imp
            elif not imp.is_used():
                yield imp

    @classmethod
    def register(
        cls, lineno: int, column: int, name: str, package: str, node: ast.AST
    ) -> None:
        _import = cls(lineno, column, name, package)
        _import.node = node
        cls.imports.append(_import)

        Scope.register(_import)

    @classmethod
    def clear(cls):
        cls.imports.clear()


@dataclass
class ImportFrom(Import):
    star: bool
    suggestions: List[str]

    def is_match_sub_packages(self, name_name):
        return False

    @classmethod
    def register(  # type: ignore
        cls,
        lineno: int,
        column: int,
        name: str,
        package: str,
        node: ast.AST,
        star: bool,
        suggestions: List[str],
    ) -> None:
        _import = cls(lineno, column, name, package, star, suggestions)
        _import.node = node
        cls.imports.append(_import)

        Scope.register(_import)


@dataclass
class Name:
    names: ClassVar[List["Name"]] = []

    lineno: int
    name: str
    is_all: bool = False

    node: ast.AST = field(init=False, repr=False, compare=False)
    match_import: Union[Import, Literal[False]] = field(
        init=False, repr=False, compare=False, default=False
    )

    @property
    def is_attribute(self):
        return "." in self.name

    def match_2(self, imp: Union[Import, ImportFrom]) -> bool:
        if self.is_all:
            is_match = self.name == imp.name
        elif self.is_attribute:
            is_match = imp.lineno < self.lineno and (
                ".".join(self.name.split(".")[: len(imp)]) == imp.name
                or imp.is_match_sub_packages(self.name)
            )
        else:
            is_match = (imp.lineno < self.lineno) and (
                self.name == imp.name or imp.is_match_sub_packages(self.name)
            )

        return is_match

    def match(self, imp: Union[Import, ImportFrom]) -> bool:
        is_match = self.match_2(imp)

        if is_match and imp.is_duplicate:
            is_match = imp.match_nearest_duplicate_import(self)

        if is_match:
            self.match_import = imp

        return is_match

    @property
    def scope(self):
        return Scope.get_scope_by_current_node(self)

    @classmethod
    def register(
        cls, lineno: int, name: str, node: ast.AST, is_all: bool = False
    ) -> None:
        _name = cls(lineno, name, is_all)
        _name.node = node
        cls.names.append(_name)

        Scope.register(_name, is_global=is_all)

    @classmethod
    def clear(cls) -> None:
        cls.names.clear()


@dataclass
class Scope:
    scopes: ClassVar[List["Scope"]] = []
    current_scope: ClassVar[List["Scope"]] = []

    node: ast.AST

    current_nodes: List[Union[Import, ImportFrom, Name]] = field(
        default_factory=list, init=False, repr=False, compare=False
    )
    parent: "Scope" = field(default=None, repr=False)
    child_scopes: Set["Scope"] = field(
        default_factory=set, init=False, repr=False, compare=False
    )

    def __hash__(self) -> int:
        return hash(self.node)

    @classmethod
    def get_curent_scope(cls) -> "Scope":
        return cls.current_scope[-1]

    @classmethod
    def get_global_scope(cls) -> "Scope":
        global_scope = cls.scopes[0]
        assert global_scope.parent is None
        return global_scope

    @classmethod
    def add_global_scope(cls, tree: ast.AST) -> None:
        parent = None
        scope = Scope(tree, parent)
        cls.current_scope.append(scope)
        cls.scopes.append(scope)  # global scope added to cls.scopes

    @classmethod
    def add_current_scope(cls, node: ast.AST) -> None:
        parent = cls.get_curent_scope()
        scope = Scope(node, parent)
        cls.current_scope.append(scope)

    @classmethod
    def remove_current_scope(cls):
        cls.current_scope.pop()

    @classmethod
    def register(
        cls, current_node: Union[Import, ImportFrom, Name], *, is_global=False
    ) -> None:
        scope = cls.get_previous_scope(
            cls.get_global_scope() if is_global else cls.get_curent_scope()
        )

        # current nodes add to scope
        scope.current_nodes.append(current_node)

        # child scopes add to scope
        if scope.parent is None:
            return

        parent = cls.get_previous_scope(scope.parent)
        child_scope = scope

        while parent:
            parent.child_scopes.add(child_scope)

            child_scope = parent
            if parent.parent is None:
                break
            parent = cls.get_previous_scope(parent.parent)

    @classmethod
    def get_scope_by_current_node(
        cls, current_node: Union[Import, ImportFrom, Name]
    ) -> "Scope":
        for scope in cls.scopes:
            if current_node in scope.current_nodes:
                return scope
        return None

    @property
    def names(self) -> Iterator[Name]:
        yield from filter(  # type: ignore
            lambda node: isinstance(node, Name), self.current_nodes
        )

        for child_scope in self.child_scopes:
            yield from child_scope.names

    @property
    def imports(self) -> Iterator[Import]:
        yield from filter(  # type: ignore
            lambda node: isinstance(node, Import), self.current_nodes
        )

    @classmethod
    def get_previous_scope(cls, scope: "Scope") -> "Scope":
        for _scope in cls.scopes:
            if _scope == scope:
                return _scope

        cls.scopes.append(scope)
        return scope

    @classmethod
    def clear(cls):
        cls.scopes.clear()
