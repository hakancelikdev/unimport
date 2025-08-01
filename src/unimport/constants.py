import ast
import sys
import sysconfig

__all__ = (
    "BUILTIN_MODULE_NAMES",
    "EXCLUDE_REGEX_PATTERN",
    "GLOB_PATTERN",
    "INCLUDE_REGEX_PATTERN",
    "INIT_FILE_IGNORE_REGEX",
    "PY39_PLUS",
    "PY310_PLUS",
    "PY312_PLUS",
    "PY313_PLUS",
    "STDLIB_PATH",
    "SUBSCRIPT_TYPE_VARIABLE",
)

# REGEX
GLOB_PATTERN = r"**/*.py"
INCLUDE_REGEX_PATTERN = r"\.(py)$"
EXCLUDE_REGEX_PATTERN = r"^$"
INIT_FILE_IGNORE_REGEX = r"__init__\.py"

# TUPLE
DEF_TUPLE = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
AST_FUNCTION_TUPLE = (ast.FunctionDef, ast.AsyncFunctionDef)

# CONF
PY39_PLUS = sys.version_info >= (3, 9)
PY310_PLUS = sys.version_info >= (3, 10)
PY312_PLUS = sys.version_info >= (3, 12)
PY313_PLUS = sys.version_info >= (3, 13)

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
        # Python >= 3.9.
        "OrderedDict",
    }
)

BUILTIN_MODULE_NAMES = sys.builtin_module_names
STDLIB_PATH = sysconfig.get_paths()["stdlib"]
