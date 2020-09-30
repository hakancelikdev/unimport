import sys
import typing

DESCRIPTION = (
    "A linter, formatter for finding and removing unused import statements."
)
VERSION = "0.3.0"

PY38_PLUS = sys.version_info >= (3, 8)
TYPE_VARIABLE_SUBSCRIPT = []

for i in dir(typing):
    try:
        eval("typing." + i + "[str]")
    except:
        pass
    else:
        TYPE_VARIABLE_SUBSCRIPT.append(i)
