from typing import TypeVar

from foo import Bar, Baz, Qux


T = TypeVar("T", bound="Bar")
U = TypeVar("U", "Baz", "Qux")
