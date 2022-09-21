import ast
import distutils.sysconfig
import sys

__all__ = (
    "BUILTIN_MODULE_NAMES",
    "EXCLUDE_REGEX_PATTERN",
    "GLOB_PATTERN",
    "INCLUDE_REGEX_PATTERN",
    "INIT_FILE_IGNORE_REGEX",
    "PY37_PLUS",
    "PY38_PLUS",
    "PY39_PLUS",
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
PY37_PLUS = sys.version_info >= (3, 7)
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

BUILTIN_MODULE_NAMES = frozenset(sys.builtin_module_names)
STDLIB_PATH = distutils.sysconfig.get_python_lib(standard_lib=True)
