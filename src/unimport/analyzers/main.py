import ast
import re
from pathlib import Path

from unimport.analyzers.import_statement import ImportAnalyzer
from unimport.analyzers.importable import ImportableNameWithScopeAnalyzer
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

        tree = ast.parse(self.source, type_comments=True)

        set_tree_parents(tree)  # set parents to tree

        Scope.add_global_scope(tree)  # add global scope of the top tree

        NameAnalyzer().traverse(tree)  # name analyzers

        ImportableNameWithScopeAnalyzer().traverse(tree)  # importable analyzers for collect in __all__

        ImportAnalyzer(  # import analyzers
            source=self.source, include_star_import=self.include_star_import, defined_names=get_defined_names(tree)
        ).traverse(tree)

        self._deduplicate_star_suggestions()
        self._cleanup_empty_type_checking()

        Scope.remove_current_scope()  # remove global scope

    def skip_file(self) -> bool:
        SKIP_FILE_REGEX = "#.*(unimport: {0,1}skip_file)"

        return bool(re.search(SKIP_FILE_REGEX, self.source, re.IGNORECASE))

    @staticmethod
    def _deduplicate_star_suggestions() -> None:
        """Remove duplicate suggestions across star and explicit imports.

        When multiple imports provide the same name, the last one wins
        (matching Python's shadowing semantics). Explicit imports also
        claim their name so star imports don't produce duplicates.
        """
        seen: set[str] = set()
        for imp in reversed(Import.imports):
            if isinstance(imp, ImportFrom) and imp.star:
                imp.suggestions = [s for s in imp.suggestions if s not in seen]
                seen.update(imp.suggestions)
            else:
                seen.add(imp.name)

    @staticmethod
    def _cleanup_empty_type_checking() -> None:
        """If all TYPE_CHECKING-guarded imports are unused, mark TYPE_CHECKING import as unused.

        Removes TYPE_CHECKING Name references so the import becomes unused,
        enabling removal of both the import and the empty if-block.
        """
        tc_imports = [imp for imp in Import.imports if imp.is_type_checking]
        if not tc_imports:
            return

        if any(imp.is_used() for imp in tc_imports):
            return

        names_to_remove = [
            name for name in Name.names if name.name == "TYPE_CHECKING" or name.name.endswith(".TYPE_CHECKING")
        ]
        for name in names_to_remove:
            Name.names.remove(name)
            for scope in Scope.scopes:
                if name in scope.current_nodes:
                    scope.current_nodes.remove(name)
                    break

    @staticmethod
    def clear():
        Name.clear()
        Import.clear()
        ImportFrom.clear()
        Scope.clear()
