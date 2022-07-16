"""It offers some utils."""
import contextlib
import difflib
import functools
import importlib.machinery
import importlib.util
import re
import tokenize
from distutils.util import strtobool
from pathlib import Path
from typing import FrozenSet, Iterable, Iterator, List, Optional, Set, Tuple

import unimport.constants as C
from unimport import typing as T

if C.PY38_PLUS:
    from importlib.metadata import (  # unimport: skip
        PackageNotFoundError,
        metadata,
    )
else:
    from importlib_metadata import PackageNotFoundError, metadata  # type: ignore

from pathspec.patterns.gitwildmatch import GitWildMatchPattern

__all__ = (
    "get_dir",
    "get_source",
    "get_spec",
    "is_std",
    "package_name_from_metadata",
    "get_used_packages",
    "actiontobool",
    "get_exclude_list_from_gitignore",
    "read",
    "list_paths",
    "diff",
    "return_exit_code",
)


def get_dir(package: str) -> FrozenSet[str]:
    try:
        module = importlib.import_module(package)
    except (ImportError, AttributeError, TypeError, ValueError):
        return frozenset()
    return frozenset(dir(module))


def get_source(package: str) -> Optional[str]:
    spec = get_spec(package)
    # The below two can be one of several values per their previous type annotations
    # But for our use case, we know that these are the specific classes that asserted to be
    if spec:
        assert isinstance(spec.loader, importlib.machinery.SourceFileLoader)
        assert isinstance(spec.loader.path, str)
        if spec.loader.path.endswith(".py"):
            return spec.loader.get_data(spec.loader.path).decode("utf-8")
    return None


@functools.lru_cache(maxsize=None)
def get_spec(package: str) -> Optional[importlib.machinery.ModuleSpec]:
    try:
        return importlib.util.find_spec(package)
    except (ImportError, AttributeError, TypeError, ValueError):
        return None


def is_std(package: str) -> bool:
    """Returns True if package module came with from Python."""

    if package in C.BUILTIN_MODULE_NAMES:
        return True
    spec = get_spec(package)
    if spec and isinstance(spec.origin, str):
        return any(
            (
                spec.origin.startswith(C.STDLIB_PATH),
                spec.origin in ("built-in", "frozen"),
                spec.origin.endswith(".so"),
            )
        )
    else:
        return False


@functools.lru_cache(maxsize=None)
def package_name_from_metadata(package: str) -> Optional[str]:
    if not is_std(package):
        with contextlib.suppress(PackageNotFoundError):
            return metadata(package)["Name"]
    return None


def get_used_packages(
    imports: List[T.ImportT], unused_imports: List[T.ImportT]
) -> Set[str]:
    packages = set()
    used_packages = set(
        map(lambda imp: imp.package.split(".")[0], imports)
    ) - set(map(lambda imp: imp.package.split(".")[0], unused_imports))
    for package in used_packages:
        name = package_name_from_metadata(package)
        if name:
            packages.add(name)
    return packages


def actiontobool(action: str) -> bool:
    if action == "":
        return True
    with contextlib.suppress(ValueError):
        return True if strtobool(action) == 1 else False
    return False


def get_exclude_list_from_gitignore() -> List[str]:
    """Converts .gitignore patterns to regex and return this exclude regex
    list."""
    path = Path(".gitignore")
    gitignore_regex: List[str] = []
    if path.is_file():
        source, _, _ = read(path)
        for line in source.splitlines():
            regex = GitWildMatchPattern.pattern_to_regex(line)[0]
            if regex:
                gitignore_regex.append(regex)
    return gitignore_regex


def read(path: Path) -> Tuple[str, str, Optional[str]]:
    try:
        with tokenize.open(path) as stream:
            source = stream.read()
            encoding = stream.encoding
            newline = stream.newlines
    except (OSError, SyntaxError):
        return "", "utf-8", None
    # If mixed or unknown newlines, fall back to the platform default
    if not isinstance(newline, str):
        newline = None
    return source, encoding, newline


def list_paths(
    start: Path,
    include: str = C.INCLUDE_REGEX_PATTERN,
    exclude: str = C.EXCLUDE_REGEX_PATTERN,
) -> Iterator[Path]:
    include_regex, exclude_regex = re.compile(include), re.compile(exclude)
    file_names: Iterable[Path]
    if start.is_dir():
        file_names = start.glob(C.GLOB_PATTERN)
    else:
        file_names = [start]
    yield from filter(
        lambda filename: include_regex.search(str(filename))
        and not exclude_regex.search(str(filename)),
        file_names,
    )


def diff(
    *, source: str, refactor_result: str, fromfile: Path = None
) -> Tuple[str, ...]:
    return tuple(
        difflib.unified_diff(
            source.splitlines(),
            refactor_result.splitlines(),
            fromfile=fromfile.as_posix() if fromfile else "",
        )
    )


def return_exit_code(
    *,
    is_unused_import_names: bool,
    is_syntax_error: bool,
    refactor_applied: bool
) -> int:
    # NOTE: If this function changes, be sure to update this page https://unimport.hakancelik.dev/#exit-code-behavior

    assert not (
        is_unused_import_names is False and refactor_applied is True
    ), "is_unused_import_names False while refactor_applied cannot be True."

    if is_syntax_error:
        return 1
    elif is_unused_import_names:
        if refactor_applied:
            return 0
        else:
            return 1
    else:
        return 0
