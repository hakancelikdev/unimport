import difflib
import re
import tokenize
from pathlib import Path

from unimport.color import Color
from unimport.config import Config
from unimport.refactor import refactor_string
from unimport.scan import Scanner


class Session:
    GLOB_PATTERN = "**/*.py"
    INCLUDE_REGEX_PATTERN = "\\.(py)$"
    EXCLUDE_REGEX_PATTERN = "^$"

    def __init__(self, config_file=None, include_star_import=False):
        self.config = Config(config_file)
        self.scanner = Scanner(include_star_import=include_star_import)

    def _read(self, path: Path):
        try:
            with tokenize.open(path) as stream:
                source = stream.read()
                encoding = stream.encoding
        except (OSError, SyntaxError) as err:
            print(Color(str(err)).red)
            return "", "utf-8"
        return source, encoding

    def _list_paths(self, start, include=None, exclude=None):
        include_regex, exclude_regex = (
            re.compile(include or self.INCLUDE_REGEX_PATTERN),
            re.compile(exclude or self.EXCLUDE_REGEX_PATTERN),
        )
        if start.is_dir():
            file_names = start.glob(self.GLOB_PATTERN)
        else:
            file_names = [start]
        yield from filter(
            lambda filename: include_regex.search(str(filename))
            and not exclude_regex.search(str(filename)),
            file_names,
        )

    def refactor(self, source: str) -> str:
        self.scanner.run_visit(source)
        refactor = refactor_string(
            source=source, unused_imports=self.scanner.unused_imports,
        )
        self.scanner.clear()
        return refactor

    def refactor_file(self, path: Path, apply: bool = False):
        source, encoding = self._read(path)
        result = self.refactor(source)
        if apply:
            path.write_text(result, encoding=encoding)
        return result

    def diff(self, source: str) -> tuple:
        return tuple(
            difflib.unified_diff(
                source.splitlines(), self.refactor(source).splitlines()
            )
        )

    def diff_file(self, path: Path) -> tuple:
        source, _ = self._read(path)
        result = self.refactor_file(path, apply=False)
        return tuple(
            difflib.unified_diff(
                source.splitlines(), result.splitlines(), fromfile=str(path)
            )
        )
