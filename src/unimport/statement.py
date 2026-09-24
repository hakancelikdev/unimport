from __future__ import annotations

import ast
import dataclasses
import typing

__all__ = ("Import", "ImportFrom", "Name", "Scope")


@dataclasses.dataclass
class Import:
    imports: typing.ClassVar[list[Import | ImportFrom]] = []

    lineno: int
    column: int
    name: str
    package: str

    node: ast.Import | ast.ImportFrom = dataclasses.field(init=False, repr=False, compare=False)
    is_type_checking: bool = dataclasses.field(init=False, repr=False, compare=False, default=False)

    def __len__(self) -> int:
        return len(self.name.split("."))

    def is_match_sub_packages(self, name_name: str) -> bool:
        return self.name.split(".")[0] == name_name.split(".")[0]

    @property
    def scope(self):
        return Scope.get_scope_by_current_node(self)

    def is_used(self) -> bool:
        for name in self.scope.names:
            if self.is_type_checking:
                if name.match_2(self):
                    return True
            elif name.match_import:
                if name.match_import == self:
                    return True
            elif name.match(self):
                return True

        return False

    def match_nearest_duplicate_import(self, name: Name) -> bool:
        nearest_import = None

        scope = name.scope
        while scope:
            imports = [
                _import
                for _import in scope.imports
                if name.match_2(_import) and name.lineno > _import.lineno and not _import.is_type_checking
            ]
            scope = scope.parent

            if imports:
                nearest_import = max(
                    filter(
                        lambda _import: _import.lineno == max(imports, key=lambda _import: _import.lineno).lineno,
                        imports,
                    ),
                    key=lambda _import: _import.column,
                )

            if nearest_import == self:
                return True

        return False

    @property
    def is_duplicate(self) -> bool:
        return [_import.name for _import in self.imports if not _import.is_type_checking].count(self.name) > 1

    @classmethod
    def get_unused_imports(cls, *, include_star_import: bool = False) -> typing.Iterator[Import | ImportFrom]:
        for imp in reversed(Import.imports):
            if include_star_import and isinstance(imp, ImportFrom) and imp.star:
                yield imp
            elif not imp.is_used():
                yield imp

    @classmethod
    def register(
        cls, *, lineno: int, column: int, name: str, package: str, node: ast.Import, is_type_checking: bool = False
    ) -> None:
        _import = cls(lineno, column, name, package)
        _import.node = node
        _import.is_type_checking = is_type_checking
        cls.imports.append(_import)

        Scope.register(_import)

    @classmethod
    def clear(cls):
        cls.imports.clear()


@dataclasses.dataclass
class ImportFrom(Import):
    star: bool
    suggestions: list[str]

    def is_match_sub_packages(self, name_name: str) -> bool:
        return False

    @classmethod
    def register(  # type: ignore[override]  # noqa
        cls,
        *,
        lineno: int,
        column: int,
        name: str,
        package: str,
        star: bool,
        suggestions: list[str],
        node: ast.ImportFrom,
        is_type_checking: bool = False,
    ) -> None:
        _import = cls(lineno, column, name, package, star, suggestions)
        _import.node = node
        _import.is_type_checking = is_type_checking
        cls.imports.append(_import)

        Scope.register(_import)


@dataclasses.dataclass
class Name:
    names: typing.ClassVar[list[Name]] = []

    lineno: int
    name: str
    is_all: bool = False

    node: ast.Name | ast.Attribute | ast.Constant = dataclasses.field(init=False, repr=False, compare=False)
    match_import: Import | ImportFrom | bool = dataclasses.field(init=False, repr=False, compare=False, default=False)

    @property
    def is_attribute(self):
        return "." in self.name

    @property
    def is_store(self) -> bool:
        """Whether this is an assignment target (``x = ...``) rather than a use.

        ``x += 1`` reads ``x`` first, so it counts as a use.
        """
        node = getattr(self, "node", None)
        return (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Store)
            and not isinstance(getattr(node, "parent", None), ast.AugAssign)
        )

    def _is_unconditional_assignment(self) -> bool:
        """``x = ...`` / ``x: T = ...`` written directly in the body of its scope."""
        statement = self.node
        while not isinstance(statement, ast.stmt):
            statement = statement.parent  # type: ignore
        if isinstance(statement, ast.AnnAssign) and statement.value is None:
            return False
        parent = getattr(statement, "parent", None)
        return (
            isinstance(statement, (ast.Assign, ast.AnnAssign))
            # Directly in a module, function or class body; not inside if/for/while/try/with/match.
            and isinstance(parent, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and statement in parent.body
        )

    def _is_rebound(self, imp: Import | ImportFrom) -> bool:
        """The import is reassigned, unconditionally and in the same scope, between the import and this use."""
        scope = self.scope
        if scope != imp.scope:
            return False
        return any(
            other.is_store
            and other.name == self.name
            and imp.lineno < other.lineno < self.lineno
            and other.scope == scope
            and other._is_unconditional_assignment()
            for other in Name.names
        )

    def _is_shadowed(self, imp: Import | ImportFrom) -> bool:
        """A function between this use and the import binds the name locally, so the use refers to that binding."""
        name = self.name.split(".")[0]
        imp_scope = imp.scope
        scope = self.scope
        while scope is not None and scope != imp_scope:
            if (
                isinstance(scope.node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and _is_in_body(self.node, scope.node)
                and name in _local_bindings(scope.node)
            ):
                return True
            scope = scope.parent
        return False

    def _is_deferred_usage(self, imp: Import | ImportFrom) -> bool:
        imp_scope = imp.scope
        scope = self.scope
        while scope is not None and scope != imp_scope:
            if isinstance(scope.node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return True
            scope = scope.parent
        return False

    def _has_more_specific_import(self, imp: Import | ImportFrom) -> bool:
        name_parts = self.name.split(".")
        for other_imp in Import.imports:
            if other_imp is imp:
                continue
            other_parts = other_imp.name.split(".")
            if len(other_parts) <= len(name_parts) and name_parts[: len(other_parts)] == other_parts:
                return True
        return False

    def match_2(self, imp: Import | ImportFrom) -> bool:
        if self.is_all:
            is_match = self.name == imp.name
        elif self.is_store:
            is_match = False
        elif self.is_attribute:
            primary_match = ".".join(self.name.split(".")[: len(imp)]) == imp.name
            sub_match = (
                not primary_match and imp.is_match_sub_packages(self.name) and not self._has_more_specific_import(imp)
            )
            is_match = (imp.lineno <= self.lineno or self._is_deferred_usage(imp)) and (primary_match or sub_match)
        else:
            is_match = (imp.lineno <= self.lineno or self._is_deferred_usage(imp)) and (
                self.name == imp.name or imp.is_match_sub_packages(self.name)
            )

        return is_match

    def match(self, imp: Import | ImportFrom) -> bool:
        is_match = self.match_2(imp)

        if is_match and not self.is_all and (self._is_shadowed(imp) or self._is_rebound(imp)):
            is_match = False

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
        cls, *, lineno: int, name: str, node: ast.Name | ast.Attribute | ast.Constant, is_all: bool = False
    ) -> None:
        _name = cls(lineno, name, is_all)
        _name.node = node
        cls.names.append(_name)

        Scope.register(_name, is_global=is_all)

    @classmethod
    def clear(cls) -> None:
        cls.names.clear()


@dataclasses.dataclass(eq=False)
class Scope:
    scopes: typing.ClassVar[list[Scope]] = []
    current_scope: typing.ClassVar[list[Scope]] = []
    # Registered scope for each AST node, keyed by id(node), so lookups don't scan cls.scopes.
    _scopes_by_node: typing.ClassVar[dict[int, Scope]] = {}

    node: ast.AST

    current_nodes: list[Import | ImportFrom | Name] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False
    )
    parent: Scope = dataclasses.field(default=None, repr=False)
    child_scopes: set[Scope] = dataclasses.field(default_factory=set, init=False, repr=False, compare=False)

    def __eq__(self, other: object) -> bool:
        # A scope is identified by its AST node. Several Scope objects can be created for the same node (the
        # current_scope stack and the registered one); they are the same scope.
        return isinstance(other, Scope) and self.node is other.node

    def __hash__(self) -> int:
        return hash(self.node)

    @classmethod
    def get_current_scope(cls) -> Scope:
        return cls.current_scope[-1]

    @classmethod
    def get_global_scope(cls) -> Scope:
        global_scope = cls.scopes[0]
        assert global_scope.parent is None
        return global_scope

    @classmethod
    def add_global_scope(cls, tree: ast.AST) -> None:
        parent = None
        scope = Scope(tree, parent)
        cls.current_scope.append(scope)
        cls.get_previous_scope(scope)  # global scope added to cls.scopes

    @classmethod
    def add_current_scope(cls, node: ast.AST) -> None:
        parent = cls.get_current_scope()
        scope = Scope(node, parent)
        cls.current_scope.append(scope)

    @classmethod
    def remove_current_scope(cls):
        cls.current_scope.pop()

    @classmethod
    def register(cls, current_node: Import | ImportFrom | Name, *, is_global=False) -> None:
        scope = cls.get_previous_scope(cls.get_global_scope() if is_global else cls.get_current_scope())

        # current nodes add to scope
        scope.current_nodes.append(current_node)
        current_node._scope = scope  # type: ignore[union-attr]

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
    def get_scope_by_current_node(cls, current_node: Import | ImportFrom | Name) -> Scope | None:
        # Set by register(). Nodes are compared by identity: dataclass equality compares fields, so two different
        # Name objects with the same line and name would be indistinguishable.
        return getattr(current_node, "_scope", None)

    @property
    def names(self) -> typing.Iterator[Name]:
        yield from filter(lambda node: isinstance(node, Name), self.current_nodes)  # type: ignore

        for child_scope in self.child_scopes:
            yield from child_scope.names

    @property
    def imports(self) -> typing.Iterator[Import]:
        yield from filter(lambda node: isinstance(node, Import), self.current_nodes)  # type: ignore

    @classmethod
    def get_previous_scope(cls, scope: Scope) -> Scope:
        registered = cls._scopes_by_node.get(id(scope.node))
        if registered is not None:
            return registered

        cls._scopes_by_node[id(scope.node)] = scope
        cls.scopes.append(scope)
        return scope

    @classmethod
    def clear(cls):
        cls.scopes.clear()
        cls._scopes_by_node.clear()


# match statements exist from Python 3.10.
_MATCH_CAPTURE_NODES = tuple(getattr(ast, name) for name in ("MatchAs", "MatchStar") if hasattr(ast, name))
_MATCH_MAPPING_NODES = tuple(getattr(ast, name) for name in ("MatchMapping",) if hasattr(ast, name))


def _is_in_body(node: ast.AST, function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Whether node is in the function body.

    Defaults, decorators and annotations are evaluated in the enclosing
    scope, although the analyzers register them in the function's
    scope.
    """
    child, parent = node, getattr(node, "parent", None)
    while parent is not None and parent is not function:
        child, parent = parent, getattr(parent, "parent", None)
    return parent is function and child in function.body


def _local_bindings(function: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    cached = getattr(function, "_unimport_local_bindings", None)
    if cached is None:
        cached = function._unimport_local_bindings = _collect_local_bindings(function)  # type: ignore[union-attr]
    return cached


def _collect_local_bindings(function: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Names that are local to a function.

    Python makes a name local to a function when it is bound anywhere in
    the function body (assignment, ``for``/``with``/``except`` target,
    ``del``, import, nested ``def``/``class``, ``match`` capture) or is
    a parameter, unless it is declared ``global`` or ``nonlocal``.
    """
    arguments = function.args
    names = {
        arg.arg
        for arg in [
            *arguments.posonlyargs,
            *arguments.args,
            *arguments.kwonlyargs,
            *filter(None, [arguments.vararg, arguments.kwarg]),
        ]
    }
    declared: set[str] = set()

    nodes: list[ast.AST] = list(function.body)
    while nodes:
        node = nodes.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
            nodes.extend(node.decorator_list)
            continue  # a nested scope
        if isinstance(node, ast.Lambda):
            continue
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            declared.update(node.names)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            if not isinstance(
                getattr(node, "parent", None), ast.comprehension
            ):  # comprehension variables are local to it
                names.add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((alias.asname or alias.name).split(".")[0] for alias in node.names if alias.name != "*")
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, _MATCH_CAPTURE_NODES) and node.name:  # type: ignore[attr-defined]
            names.add(node.name)  # type: ignore[attr-defined]
        elif isinstance(node, _MATCH_MAPPING_NODES) and node.rest:  # type: ignore[attr-defined]
            names.add(node.rest)  # type: ignore[attr-defined]
        nodes.extend(ast.iter_child_nodes(node))

    return frozenset(names - declared)
