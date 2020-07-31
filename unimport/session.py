import difflib
import re
import tokenize
from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple

from unimport.color import Color
from unimport.config import CONFIG_FILES, Config
from unimport.refactor import refactor_string
from unimport.scan import Scanner


class Session:
    GLOB_PATTERN = "**/*.py"
    INCLUDE_REGEX_PATTERN = "\\.(py)$"
    EXCLUDE_REGEX_PATTERN = "^$"

    def __init__(
        self,
        config_file: Optional[Path] = None,
        *,
        include_star_import: bool = False,
        show_error: bool = False
    ) -> None:
        self.show_error = show_error
        self.config = (
            Config(config_file)
            if config_file and config_file.name in CONFIG_FILES
            else None
        )
        self.scanner = Scanner(
            include_star_import=include_star_import, show_error=self.show_error
        )

    def read(self, path: Path) -> Tuple[str, str]:
        try:
            with tokenize.open(path) as stream:
                source = stream.read()
                encoding = stream.encoding
        except (OSError, SyntaxError) as err:
            if self.show_error:
                print(Color(str(err)).red)
            return "", "utf-8"
        return source, encoding

    def list_paths(
        self,
        start: Path,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Iterator[Path]:
        include_regex, exclude_regex = (
            re.compile(include or self.INCLUDE_REGEX_PATTERN),
            re.compile(exclude or self.EXCLUDE_REGEX_PATTERN),
        )
        file_names: Iterable[Path]
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
        self.scanner.scan(source)
        refactor = refactor_string(
            source=source,
            unused_imports=self.scanner.unused_imports,
            show_error=self.show_error,
        )
        self.scanner.clear()
        return refactor

    def refactor_file(self, path: Path, apply: bool = False) -> str:
        source, encoding = self.read(path)
        result = self.refactor(source)
        if apply:
            path.write_text(result, encoding=encoding)
        return result

    def diff(self, source: str) -> Tuple[str, ...]:
        return tuple(
            difflib.unified_diff(
                source.splitlines(), self.refactor(source).splitlines()
            )
        )

    def diff_file(self, path: Path) -> Tuple[str, ...]:
        source, _ = self.read(path)
        result = self.refactor_file(path, apply=False)
        return tuple(
            difflib.unified_diff(
                source.splitlines(), result.splitlines(), fromfile=str(path)
            )
        )
