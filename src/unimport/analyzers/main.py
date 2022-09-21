import ast
import re
from pathlib import Path

from unimport import constants as C
from unimport.analyzers.import_statement import ImportAnalyzer
from unimport.analyzers.importable import ImportableAnalyzer
from unimport.analyzers.name import NameAnalyzer
from unimport.analyzers.utils import get_defined_names, set_tree_parents
from unimport.statement import Import, ImportFrom, Name, Scope

__all__ = ("MainAnalyzer",)


class MainAnalyzer(ast.NodeVisitor):
    __slots__ = ("source", "path", "include_star_import")

    def __init__(self, *, source: str, path: Path = Path("<unknown file>"), include_star_import: bool = False):
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

        set_tree_parents(tree)  # set parents to tree

        Scope.add_global_scope(tree)  # add global scope of the top tree

        NameAnalyzer().traverse(tree)  # name analyzers

        ImportableAnalyzer().traverse(tree)  # importable analyzers for collect in __all__

        ImportAnalyzer(  # import analyzers
            source=self.source, include_star_import=self.include_star_import, defined_names=get_defined_names(tree)
        ).traverse(tree)

        Scope.remove_current_scope()  # remove global scope

    def skip_file(self) -> bool:
        SKIP_FILE_REGEX = "#.*(unimport: {0,1}skip_file)"

        return bool(re.search(SKIP_FILE_REGEX, self.source, re.IGNORECASE))

    @staticmethod
    def clear():
        Name.clear()
        Import.clear()
        ImportFrom.clear()
        Scope.clear()
