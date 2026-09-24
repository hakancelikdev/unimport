from __future__ import annotations

import dataclasses
import functools
import json
import typing
from concurrent.futures import ProcessPoolExecutor
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
    refactor_result: str | None = dataclasses.field(default=None, repr=False)
    syntax_error: str | None = None
    read_error: str | None = None  # the file could not be read; nothing else is set


def _analyze_path(
    path: Path,
    *,
    include_star_import: bool,
    refactor: bool,
    is_ignored_import: typing.Callable[[Path, str], bool] | None = None,
) -> _Result:
    """Analyze a single file.

    This runs in a worker process when ``--jobs`` is greater than one,
    so it must be a module-level function and return a picklable
    result. The analyzers keep their state on class attributes, which
    is why each file is fully analyzed and cleared before the next one.
    """
    from unimport.refactor import refactor_string

    try:
        source, encoding, newline = utils.read(path)
    except utils.READ_ERRORS as exc:
        return _Result([], path, "", "utf-8", read_error=str(exc))

    analyzer = MainAnalyzer(source=source, path=path, include_star_import=include_star_import)
    syntax_error = None
    try:
        analyzer.traverse()
    except SyntaxError as exc:
        syntax_error = str(exc)

    try:
        unused_imports = [
            imp
            for imp in Import.get_unused_imports(include_star_import=include_star_import)
            # per-file-ignores; filtered before refactoring so ignored imports are never removed
            if not (is_ignored_import and is_ignored_import(path, imp.name))
        ]
    finally:
        analyzer.clear()

    for imp in unused_imports:
        # The AST node (and the scope, which holds one) links to the whole parsed tree. Neither is needed after
        # analysis, and they would make the result expensive (or impossible, for deeply nested trees) to send back
        # from a worker process.
        vars(imp).pop("node", None)
        vars(imp).pop("_scope", None)

    refactor_result = refactor_string(source=source, unused_imports=unused_imports) if refactor else None
    return _Result(unused_imports, path, source, encoding, newline, refactor_result, syntax_error)


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

    def _analyze_paths(self) -> typing.Iterator[_Result]:
        analyze = functools.partial(
            _analyze_path,
            include_star_import=self.config.include_star_import,
            refactor=self.config.diff or self.config.remove,
            is_ignored_import=self.config.is_ignored_import,
        )
        paths = list(self.config.get_paths())
        jobs = min(self.config.jobs, len(paths))
        if jobs <= 1:
            yield from map(analyze, paths)
            return

        # Results come back in input order, so the output is the same as a sequential run.
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            yield from executor.map(analyze, paths, chunksize=max(1, len(paths) // (jobs * 4)))

    def report_error(self, message: str, path: Path) -> None:
        """Report a file that can't be read or parsed; the exit code becomes 1."""
        if self.is_json:
            self.json_report["errors"].append({"path": path.as_posix(), "message": message})
        else:
            print(
                paint(message, Color.RED, self.config.use_color)
                + " at "
                + paint(path.as_posix(), Color.GREEN, self.config.use_color)
            )
        self.is_syntax_error = True

    def get_results(self) -> typing.Iterator[_Result]:
        for result in self._analyze_paths():
            if result.read_error is not None:
                self.report_error(result.read_error, result.path)
                continue
            if result.syntax_error is not None:
                self.report_error(result.syntax_error, result.path)

            if self.is_unused_imports is False:
                self.is_unused_imports = result.unused_imports != []

            yield result

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

    def permission(self, result: _Result) -> bool:
        return commands.permission(result.path, self.config.use_color)

    @classmethod
    def run(cls, argv: typing.Sequence[str] | None = None) -> Main:
        self = cls(argv)
        for result in self.get_results():
            if self.config.check:
                self.check(result)
            if any((self.config.diff, self.config.remove)):
                refactor_result = typing.cast(str, result.refactor_result)
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
