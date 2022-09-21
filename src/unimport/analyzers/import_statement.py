import ast
from typing import List, Set

from unimport import constants as C
from unimport import typing as T
from unimport.analyzers.decarators import generic_visit, skip_import
from unimport.analyzers.defined_name import DefinedNameAnalyzer
from unimport.analyzers.importable import ImportableAnalyzer
from unimport.relate import first_occurrence
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("ImportAnalyzer",)


class ImportAnalyzer(ast.NodeVisitor):
    __slots__ = (
        "source",
        "include_star_import",
        "any_import_error",
        "defined_names",
    )

    ignore_modules_imports = ("__future__",)
    skip_import_comments_regex = "#.*(unimport: {0,1}skip|noqa)"

    def __init__(self, *, source: str, include_star_import: bool = False):
        self.source = source
        self.include_star_import = include_star_import

        self.any_import_error = False
        self.defined_names: Set[str] = set()

    def traverse(self, tree) -> None:
        defined_name_scanner = DefinedNameAnalyzer()
        defined_name_scanner.visit(tree)
        self.defined_names = defined_name_scanner.defined_names

        self.visit(tree)

    def visit_ClassDef(self, node) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    def visit_FunctionDef(self, node: T.ASTFunctionT) -> None:
        Scope.add_current_scope(node)

        self.generic_visit(node)

        Scope.remove_current_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    @generic_visit
    @skip_import
    def visit_Import(self, node: ast.Import) -> None:
        if_names, orelse_names = set(), set()

        if_node = first_occurrence(node, (ast.If,))
        if if_node:
            if_names = {
                name.asname or name.name
                for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.body)
                for name in n.names
            }
            orelse_names = {
                name.asname or name.name
                for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.orelse)
                for name in n.names
            }

        for column, alias in enumerate(node.names):
            name = alias.asname or alias.name
            if name in if_names and name in orelse_names:
                continue

            if name in C.IGNORE_IMPORT_NAMES:
                continue

            Import.register(lineno=node.lineno, column=column + 1, name=name, package=alias.name, node=node)

    @generic_visit
    @skip_import
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if_names, orelse_names = set(), set()

        if_node = first_occurrence(node, (ast.If,))
        if if_node:
            if_names = {
                name.asname or name.name
                for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.body)
                for name in n.names
            }
            orelse_names = {
                name.asname or name.name
                for n in filter(lambda node: isinstance(node, (ast.Import, ast.ImportFrom)), if_node.orelse)
                for name in n.names
            }

        is_star = node.names[0].name == "*"
        for column, alias in enumerate(node.names):
            package = node.module if not node.level else "." * node.level + str(node.module) or ""
            if (package in self.ignore_modules_imports) or (is_star and not self.include_star_import):
                return

            name = package if is_star else (alias.asname or alias.name)
            if name in if_names and name in orelse_names:
                continue

            if name in C.IGNORE_IMPORT_NAMES:
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

    def visit_Try(self, node: ast.Try) -> None:
        self.any_import_error = True

        self.generic_visit(node)

        self.any_import_error = False

    def get_suggestions(self, package: str) -> List[str]:
        names = set(map(lambda name: name.name.split(".")[0], Name.names))
        from_names = ImportableAnalyzer.get_names(package)
        return sorted(from_names & (names - self.defined_names))
