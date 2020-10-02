"""It offers some utils according to the import name."""

import distutils.sysconfig
import functools
import importlib
import importlib.machinery
import importlib.util
import sys
from typing import FrozenSet, Optional

BUILTIN_MODULE_NAMES = frozenset(sys.builtin_module_names)
STDLIB_PATH = distutils.sysconfig.get_python_lib(standard_lib=True)


def get_dir(import_name: str) -> FrozenSet[str]:
    try:
        module = importlib.import_module(import_name)
    except (ImportError, AttributeError, TypeError, ValueError):
        return frozenset()
    return frozenset(dir(module))


def get_source(import_name: str) -> Optional[str]:
    spec = get_spec(import_name)
    # The below two can be one of several values per their previous type annotations
    # But for our use case, we know that these are the specific classes that asserted to be
    if spec:
        assert isinstance(spec.loader, importlib.machinery.SourceFileLoader)
        assert isinstance(spec.loader.path, str)
        if spec.loader.path.endswith(".py"):
            return spec.loader.get_data(spec.loader.path).decode("utf-8")
    return None


@functools.lru_cache(maxsize=None)
def get_spec(import_name: str) -> Optional[importlib.machinery.ModuleSpec]:
    try:
        return importlib.util.find_spec(import_name)
    except (ImportError, AttributeError, TypeError, ValueError):
        return None


def is_std(import_name: str) -> bool:
    """Returns True if import_name module came with from Python."""

    if import_name in BUILTIN_MODULE_NAMES:
        return True
    spec = get_spec(import_name)
    return bool(spec) and any(
        (
            spec.origin.startswith(STDLIB_PATH),
            spec.origin in ["built-in", "frozen"],
            spec.origin.endswith(".so"),
        )
    )
