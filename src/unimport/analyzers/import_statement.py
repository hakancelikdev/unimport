import ast
from typing import List, Optional, Set

from unimport.analyzers.decarators import generic_visit, skip_import
from unimport.analyzers.importable import ImportableAnalyzer
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("ImportAnalyzer",)


class ImportAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "source",
        "include_star_import",
        "any_import_error",
        "defined_names",
    )

    IGNORE_MODULES_IMPORTS = ("__future__",)
    IGNORE_IMPORT_NAMES = ("__all__", "__doc__", "__name__")

    def __init__(
        self, *, source: str, include_star_import: bool = False, defined_names: Optional[Set[str]] = None
    ) -> None:
        self.source = source
        self.include_star_import = include_star_import
        self.defined_names = defined_names or set()

        self.any_import_error = False

        self.if_names: Set[str] = set()
        self.orelse_names: Set[str] = set()

    def traverse(self, tree) -> None:
        self.visit(tree)

    def scope_analysis(self, node):
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_ClassDef = scope_analysis
    visit_FunctionDef = scope_analysis
    visit_AsyncFunctionDef = scope_analysis

    @generic_visit
    @skip_import
    def visit_Import(self, node: ast.Import) -> None:
        for column, alias in enumerate(node.names):
            name = alias.asname or alias.name
            if name in self.IGNORE_IMPORT_NAMES or (name in self.if_names and name in self.orelse_names):
                continue

            Import.register(lineno=node.lineno, column=column + 1, name=name, package=alias.name, node=node)

    @generic_visit
    @skip_import
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        is_star = node.names[0].name == "*"

        for column, alias in enumerate(node.names):
            package = node.module if not node.level else "." * node.level + str(node.module) or ""
            if (package in self.IGNORE_MODULES_IMPORTS) or (is_star and not self.include_star_import):
                return

            name = package if is_star else (alias.asname or alias.name)
            if name in self.IGNORE_IMPORT_NAMES or (name in self.if_names and name in self.orelse_names):
                continue

            ImportFrom.register(
                lineno=node.lineno,
                column=column + 1,
                name=name,
                package=package,
                star=is_star,
                suggestions=self.get_suggestions(package) if is_star else [],
                node=node,
            )

    def visit_If(self, if_node: ast.If) -> None:
        self.if_names = {
            name.asname or name.name
            for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.body)
            for name in n.names  # type: ignore
        }

        self.orelse_names = {
            name.asname or name.name
            for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.orelse)
            for name in n.names  # type: ignore
        }

        self.generic_visit(if_node)

        self.if_names = set()
        self.orelse_names = set()

    def visit_Try(self, node: ast.Try) -> None:
        self.any_import_error = True

        self.generic_visit(node)

        self.any_import_error = False

    def get_suggestions(self, package: str) -> List[str]:
        names = set(map(lambda name: name.name.split(".")[0], Name.names))
        from_names = ImportableAnalyzer.get_names(package)
        return sorted(from_names & (names - self.defined_names))
