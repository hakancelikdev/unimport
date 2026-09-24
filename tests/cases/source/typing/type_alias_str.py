import typing
from typing import TypeAlias

from foo import Bar, Baz


Alias: TypeAlias = "Bar"
Other: typing.TypeAlias = "list[Baz]"
