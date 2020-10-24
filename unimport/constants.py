import ast
import builtins
import distutils.sysconfig
import sys
from typing import Any, Callable, TypeVar, Union

from unimport.statement import Import, ImportFrom

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.6.6"

PY38_PLUS = sys.version_info >= (3, 8)

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

INITIAL_IMPORTS = frozenset(
    # https://docs.python.org/3/library/sys.html#sys.modules
    # The first thing Python will do is look up the name of import in sys.modules.
    # Initial modules are below.
    {
        "encodings.utf_8",
        "encodings.aliases",
        "encodings.latin_1",
        "importlib._bootstrap",
        "importlib.abc",
        "importlib.machinery",
        "importlib._bootstrap_external",
        "importlib.util",
        "os.path",
    }
)

IGNORE_IMPORT_NAMES = frozenset({"__all__", "__doc__", "__name__"})
BUILTINS = frozenset(dir(builtins))

Function = TypeVar("Function", bound=Callable[..., Any])
ASTImportableT = Union[
    ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name, ast.alias
]
ASTFunctionT = Union[ast.FunctionDef, ast.AsyncFunctionDef]
ImportT = Union[Import, ImportFrom]
CFNT = Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name]
DefTuple = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
ASTFunctionTuple = (ast.FunctionDef, ast.AsyncFunctionDef)
BUILTIN_MODULE_NAMES = frozenset(sys.builtin_module_names)
STDLIB_PATH = distutils.sysconfig.get_python_lib(standard_lib=True)
