import ast
import builtins
import distutils.sysconfig
import sys
from typing import Any, Callable, TypeVar, Union

from unimport.statement import Import, ImportFrom

__all__ = [
    "DESCRIPTION",
    "VERSION",
    "PY38_PLUS",
    "SUBSCRIPT_TYPE_VARIABLE",
    "IGNORE_IMPORT_NAMES",
    "BUILTINS",
    "Function",
    "ASTImportableT",
    "ASTFunctionT",
    "ImportT",
    "CFNT",
    "DefTuple",
    "ASTFunctionTuple",
    "BUILTIN_MODULE_NAMES",
    "STDLIB_PATH",
    "GLOB_PATTERN",
    "INCLUDE_REGEX_PATTERN",
    "EXCLUDE_REGEX_PATTERN",
    "INIT_FILE_IGNORE_REGEX",
]

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.7.4"

PY38_PLUS = sys.version_info >= (3, 8)
PY39_PLUS = sys.version_info >= (3, 9)

SUBSCRIPT_TYPE_VARIABLE = frozenset(
    {
        "AbstractSet",
        "AsyncContextManager",
        "AsyncGenerator",
        "AsyncIterable",
        "AsyncIterator",
        "Awaitable",
        "Callable",
        "ChainMap",
        "ClassVar",
        "Collection",
        "Container",
        "ContextManager",
        "Coroutine",
        "Counter",
        "DefaultDict",
        "Deque",
        "Dict",
        "FrozenSet",
        "Generator",
        "IO",
        "ItemsView",
        "Iterable",
        "Iterator",
        "KeysView",
        "List",
        "Mapping",
        "MappingView",
        "Match",
        "MutableMapping",
        "MutableSequence",
        "MutableSet",
        "Optional",
        "Pattern",
        "Reversible",
        "Sequence",
        "Set",
        "SupportsRound",
        "Tuple",
        "Type",
        "Union",
        "ValuesView",
        # Python >= 3.7.
        "Literal",
        # Python >= 3.8.
        "OrderedDict",
    }
)

IGNORE_IMPORT_NAMES = frozenset({"__all__", "__doc__", "__name__"})
BUILTINS = frozenset(dir(builtins))

Function = TypeVar("Function", bound=Callable[..., Any])
ASTImportableT = Union[
    ast.AsyncFunctionDef,
    ast.Attribute,
    ast.ClassDef,
    ast.FunctionDef,
    ast.Name,
    ast.alias,
]

ASTFunctionT = Union[ast.FunctionDef, ast.AsyncFunctionDef]
ImportT = Union[Import, ImportFrom]
CFNT = Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name]
DefTuple = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
ASTFunctionTuple = (ast.FunctionDef, ast.AsyncFunctionDef)
BUILTIN_MODULE_NAMES = frozenset(sys.builtin_module_names)
STDLIB_PATH = distutils.sysconfig.get_python_lib(standard_lib=True)
GLOB_PATTERN = r"**/*.py"
INCLUDE_REGEX_PATTERN = r"\.(py)$"
EXCLUDE_REGEX_PATTERN = r"^$"
INIT_FILE_IGNORE_REGEX = r"__init__\.py"
