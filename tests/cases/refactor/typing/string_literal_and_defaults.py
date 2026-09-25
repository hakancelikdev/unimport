from decimal import Decimal
from fractions import Fraction
from typing import Annotated, Literal, ParamSpec, TypeVar

T = TypeVar("T", default="Decimal")
P = ParamSpec("P", default="Fraction")
mode: Literal["Number"] = "Number"
amount: Annotated[int, "Decimal"] = 1
