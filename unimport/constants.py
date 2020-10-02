import sys

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.3.0"

PY38_PLUS = sys.version_info >= (3, 8)
PY37_PLUS = sys.version_info >= (3, 7)

SUBSCRIPT_TYPE_VARIABLE = [
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
]

if PY38_PLUS:
    SUBSCRIPT_TYPE_VARIABLE.extend(["Literal", "OrderedDict"])
elif PY37_PLUS:
    SUBSCRIPT_TYPE_VARIABLE.append("Literal")
