import difflib
import re
import tokenize
from pathlib import Path

from unimport.config import Config
from unimport.refactor import refactor_string
from unimport.scan import Scanner


class Session:
    PATTERN = "**/*.py"

    def __init__(self, config_file=None, include_star_import=False):
        self.config = Config(config_file)
        self.scanner = Scanner(include_star_import=include_star_import)

    def _read(self, path: Path):
        try:
            with tokenize.open(path) as stream:
                source = stream.read()
                encoding = stream.encoding
        except OSError as exc:
            print(f"{exc} Can't read")
            return "", "utf-8"
        except SyntaxError as exc:
            print(f"{exc} Can't read")
            return "", "utf-8"
        return source, encoding

    def _list_paths(self, start: Path, include: str, exclude: str):
        include_regex, exclude_regex = re.compile(include), re.compile(exclude)
        return [
            filename
            for filename in start.glob(self.PATTERN)
            if include_regex.search(str(filename))
            if not exclude_regex.search(str(filename))
        ]

    def refactor(self, source: str) -> str:
        self.scanner.run_visit(source)
        refactor = refactor_string(
            source=source,
            unused_imports=list(self.scanner.get_unused_imports()),
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
