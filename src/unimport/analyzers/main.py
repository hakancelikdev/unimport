import ast
import re
from pathlib import Path

from unimport import constants as C
from unimport.analyzers.import_statement import ImportAnalyzer
from unimport.analyzers.importable import ImportableAnalyzer
from unimport.analyzers.name import NameAnalyzer
from unimport.relate import relate
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("MainAnalyzer",)


class MainAnalyzer(ast.NodeVisitor):
    __slots__ = ("source", "path", "include_star_import")

    skip_file_regex = "#.*(unimport: {0,1}skip_file)"

    def __init__(
        self,
        *,
        source: str,
        path: Path = Path("<unknown file>"),
        include_star_import: bool = False,
    ):
        self.source = source
        self.path = path
        self.include_star_import = include_star_import

    def __enter__(self):
        self.traverse()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.clear()

    def traverse(self) -> None:
        if self.skip_file():
            return None

        tree = ast.parse(self.source, type_comments=True) if C.PY38_PLUS else ast.parse(self.source)
        """
        Set parent
        """
        relate(tree)

        Scope.add_global_scope(tree)

        """
        Name analyzer
        """
        NameAnalyzer().visit(tree)
        """
        Receive items on the __all__ list
        """
        importable_visitor = ImportableAnalyzer()
        importable_visitor.visit(tree)
        for node in importable_visitor.importable_nodes:
            if isinstance(node, ast.Constant):
                Name.register(
                    lineno=node.lineno,
                    name=str(node.value),
                    node=node,
                    is_all=True,
                )
            elif isinstance(node, ast.Str):
                Name.register(lineno=node.lineno, name=node.s, node=node, is_all=True)
        importable_visitor.clear()
        """
        Import analyzer
        """
        ImportAnalyzer(source=self.source, include_star_import=self.include_star_import).traverse(tree)

        Scope.remove_current_scope()

    def skip_file(self) -> bool:
        return bool(re.search(self.skip_file_regex, self.source, re.IGNORECASE))

    @staticmethod
    def clear():
        Name.clear()
        Import.clear()
        ImportFrom.clear()
        Scope.clear()
