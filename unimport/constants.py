import sys
import typing

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.3.0"

PY38_PLUS = sys.version_info >= (3, 8)
PY37_PLUS = sys.version_info >= (3, 7)
PY36_PLUS = sys.version_info >= (3, 6)

PY36 = PY36_PLUS and not PY37_PLUS

if PY37_PLUS:
    _TypeAncestors = (typing._GenericAlias, typing._SpecialForm)  # type: ignore
elif PY36_PLUS:
    _TypeAncestors = (typing.GenericMeta,)  # type: ignore

_typing_variables = [
    type_name for type_name in dir(typing) if not type_name.startswith("_")
]
SUBSCRIPT_TYPE_VARIABLE = [
    type_name
    for type_name in _typing_variables
    if isinstance(getattr(typing, type_name), _TypeAncestors)
]

if PY36:
    SUBSCRIPT_TYPE_VARIABLE.extend(
        [
            "Callable",
            "ClassVar",
            "Optional",
            "Tuple",
            "Type",
            "Union",
        ]
    )
