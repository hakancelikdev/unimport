from __future__ import annotations

import contextlib
import dataclasses
import json
import typing
from pathlib import Path

from unimport import commands
from unimport import constants as C
from unimport import utils
from unimport.analyzers import MainAnalyzer
from unimport.color import paint
from unimport.config import Config
from unimport.enums import Color
from unimport.statement import Import, ImportFrom

__all__ = ("Main",)


@dataclasses.dataclass
class _Result:
    unused_imports: list[Import | ImportFrom] = dataclasses.field(repr=False)
    path: Path
    source: str
    encoding: str
    newline: str | None = None


@dataclasses.dataclass
class Main:
    argv: typing.Sequence[str] | None = None

    config: Config = dataclasses.field(init=False)
    is_syntax_error: bool = dataclasses.field(init=False, default=False)
    json_report: dict = dataclasses.field(
        init=False, repr=False, default_factory=lambda: {"unused_imports": [], "errors": []}
    )
    is_unused_imports: bool = dataclasses.field(init=False, default=False)
    refactor_applied: bool = dataclasses.field(init=False, default=False)

    def __post_init__(self):
        self.config = self.argv_to_config()

    def argv_to_config(self) -> Config:
        import sys

        from unimport.config import ParseConfig

        parser = commands.generate_parser()
        args = parser.parse_args(self.argv if self.argv is not None else sys.argv[1:])
        try:
            return ParseConfig.parse_args(args)
        except ValueError as exc:  # invalid option combination or value
            parser.error(str(exc))

    @contextlib.contextmanager
    def analysis(self, source: str, path: Path) -> typing.Iterator:
        analyzer = MainAnalyzer(
            source=source,
            path=path,
            include_star_import=self.config.include_star_import,
        )
        try:
            analyzer.traverse()
        except SyntaxError as exc:
            if self.is_json:
                self.json_report["errors"].append({"path": path.as_posix(), "message": str(exc)})
            else:
                print(
                    paint(str(exc), Color.RED, self.config.use_color)
                    + " at "
                    + paint(path.as_posix(), Color.GREEN, self.config.use_color)
                )
            self.is_syntax_error = True

        try:
            yield
        finally:
            analyzer.clear()

    def get_results(self) -> typing.Iterator[_Result]:
        for path in self.config.get_paths():
            source, encoding, newline = utils.read(path)

            with self.analysis(source, path):
                unused_imports = list(Import.get_unused_imports(include_star_import=self.config.include_star_import))
                if self.is_unused_imports is False:
                    self.is_unused_imports = unused_imports != []

                yield _Result(unused_imports, path, source, encoding, newline)

    @property
    def is_json(self) -> bool:
        return self.config.format == C.OUTPUT_FORMAT_JSON

    def check(self, result: _Result) -> None:
        if self.is_json:
            self.json_report["unused_imports"].extend(
                {
                    "path": result.path.as_posix(),
                    "line": imp.lineno,
                    "name": imp.name,
                    "package": imp.package,
                    "star": isinstance(imp, ImportFrom) and imp.star,
                    "suggestions": imp.suggestions if isinstance(imp, ImportFrom) else [],
                }
                # sorted by line: unused imports are collected bottom-up
                for imp in sorted(result.unused_imports, key=lambda imp: (imp.lineno, imp.column))
            )
        else:
            commands.check(result.path, result.unused_imports, self.config.use_color)

    def remove(self, result: _Result, refactor_result):
        commands.remove(
            result.path,
            result.encoding,
            result.newline,
            refactor_result,
            self.config.use_color,
        )
        self.refactor_applied = True

    def diff(self, result, refactor_result):
        return commands.diff(result.path, result.source, refactor_result, self.config.use_color)

    @staticmethod
    def permission(result) -> bool:
        return commands.permission(result.path, result.encoding)

    @classmethod
    def run(cls, argv: typing.Sequence[str] | None = None) -> Main:
        from unimport.refactor import refactor_string

        self = cls(argv)
        for result in self.get_results():
            if self.config.check:
                self.check(result)
            if any((self.config.diff, self.config.remove)):
                refactor_result = refactor_string(source=result.source, unused_imports=result.unused_imports)
                if self.config.diff:
                    exists_diff = self.diff(result, refactor_result)
                    if self.config.permission and exists_diff:
                        self.config.remove = self.permission(result)
                if self.config.remove and result.source != refactor_result:
                    self.remove(result, refactor_result)
        if self.is_json:
            print(json.dumps(self.json_report, indent=2, ensure_ascii=False))
        return self

    def exit_code(self):
        from unimport.utils import return_exit_code

        return return_exit_code(
            is_unused_imports=self.is_unused_imports,
            is_syntax_error=self.is_syntax_error,
            refactor_applied=self.refactor_applied,
        )
