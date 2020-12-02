"""It offers some utils."""
import contextlib
import functools
import importlib
import importlib.machinery  # unimport: skip
import importlib.util  # unimport: skip
import io
import tokenize
from distutils.util import strtobool
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Set

from importlib_metadata import PackageNotFoundError, metadata
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

from unimport import constants as C


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
                spec.origin in ["built-in", "frozen"],
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
    imports: List[C.ImportT], unused_imports: List[C.ImportT]
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
        return strtobool(action)
    return False


def get_exclude_list_from_gitignore() -> List[str]:
    """Converts .gitignore patterns to regex and return this exclude regex
    list."""
    path = Path(".gitignore")
    gitignore_regex: List[str] = []
    if path.is_file():
        for line in tokenize.open(path).readlines():
            regex = GitWildMatchPattern.pattern_to_regex(line)[0]
            if regex:
                gitignore_regex.append(regex)
    return gitignore_regex


@functools.lru_cache(maxsize=None)
def recover_comments(text: str) -> Dict[int, str]:
    comments = {}
    with contextlib.suppress(tokenize.TokenError):
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comments[token.start[0]] = token.string
    return comments
