import contextlib
import dataclasses
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, List, Optional, Sequence, Union

from unimport import color, commands, utils
from unimport.analyzer import Analyzer
from unimport.config import Config
from unimport.statement import Import

if TYPE_CHECKING:
    from unimport.statement import ImportFrom


__all__ = ("Main",)


@dataclasses.dataclass
class _Result:
    unused_imports: List[Union["Import", "ImportFrom"]] = dataclasses.field(
        repr=False
    )
    path: Path
    source: str
    encoding: str
    newline: Optional[str] = None


@dataclasses.dataclass
class Main:
    argv: Optional[Sequence[str]] = None

    config: Config = dataclasses.field(init=False)
    is_syntax_error: bool = dataclasses.field(init=False, default=False)
    is_unused_imports: bool = dataclasses.field(init=False, default=False)
    refactor_applied: bool = dataclasses.field(init=False, default=False)

    def __post_init__(self):
        self.config = self.argv_to_config()

    def argv_to_config(self) -> Config:
        import sys

        from unimport.config import ParseConfig

        return ParseConfig.parse_args(
            commands.generate_parser().parse_args(
                self.argv if self.argv is not None else sys.argv[1:]
            )
        )

    @contextlib.contextmanager
    def analysis(self, source: str, path: Path) -> Iterator:
        analysis = Analyzer(
            source=source,
            path=path,
            include_star_import=self.config.include_star_import,
        )
        try:
            analysis.traverse()
        except SyntaxError as exc:
            print(
                color.paint(str(exc), color.RED, self.config.use_color)
                + " at "
                + color.paint(
                    path.as_posix(), color.GREEN, self.config.use_color
                )
            )
            self.is_syntax_error = True

        try:
            yield
        finally:
            analysis.clear()

    def get_results(self) -> Iterator[_Result]:
        for path in self.config.get_paths():
            source, encoding, newline = utils.read(path)

            with self.analysis(source, path):
                unused_imports = list(
                    Import.get_unused_imports(self.config.include_star_import)
                )
                if self.is_unused_imports is False:
                    self.is_unused_imports = unused_imports != []

                yield _Result(unused_imports, path, source, encoding, newline)

    def check(self, result: _Result) -> None:
        commands.check(
            result.path, result.unused_imports, self.config.use_color
        )

    def remove(self, result: _Result, refactor_result):
        commands.remove(
            result.path,
            result.encoding,
            result.newline,
            refactor_result,
            self.config.use_color,
        )
        self.refactor_applied = True

    @staticmethod
    def diff(result, refactor_result):
        return commands.diff(result.path, result.source, refactor_result)

    def permission(self, result, refactor_result):
        commands.permission(
            result.path,
            result.encoding,
            result.newline,
            refactor_result,
            self.config.use_color,
        )

    @classmethod
    def run(cls, argv: Optional[Sequence[str]] = None) -> "Main":
        from unimport.refactor import refactor_string

        self = cls(argv)
        for result in self.get_results():
            if self.config.check:
                self.check(result)
            if any((self.config.diff, self.config.remove)):
                refactor_result = refactor_string(
                    source=result.source, unused_imports=result.unused_imports
                )
                if self.config.diff:
                    exists_diff = self.diff(result, refactor_result)
                    if self.config.permission and exists_diff:
                        self.permission(result, refactor_result)
                if self.config.remove and result.source != refactor_result:
                    self.remove(result, refactor_result)
        return self

    def exit_code(self):
        from unimport.utils import return_exit_code

        return return_exit_code(
            is_unused_imports=self.is_unused_imports,
            is_syntax_error=self.is_syntax_error,
            refactor_applied=self.refactor_applied,
        )
