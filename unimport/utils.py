"""It offers some utils according to the import name."""

import distutils.sysconfig
import importlib
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
    if spec and spec.loader.path.endswith(".py"):
        return spec.loader.get_data(spec.loader.path).decode("utf-8")
    return None


def get_spec(import_name: str):
    try:
        return importlib.util.find_spec(import_name)  # type: ignore
    except (ImportError, AttributeError, TypeError, ValueError):
        return None


def is_std(import_name: str) -> bool:
    """Returns True if import_name module came with from Python."""

    if import_name in BUILTIN_MODULE_NAMES:
        return True
    spec = get_spec(import_name)
    if spec:
        return any(
            (
                spec.origin.startswith(STDLIB_PATH),
                spec.origin in ["built-in", "frozen"],
                spec.origin.endswith(".so"),
            )
        )
    return False
