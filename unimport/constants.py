import sys

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.3.0"

PY38_PLUS = sys.version_info >= (3, 8)

SUBSCRIPT_TYPE_VARIABLE = {
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
