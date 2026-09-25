# pytest.mark.skipif(not PY313_PLUS, reason: "type parameter defaults are supported above python 3.13")

from decimal import Decimal
from fractions import Fraction
from numbers import Number
from typing import Protocol

type Money = "Decimal"


def scale[T: "Fraction" = "Number"](value: T) -> T:
    return value


class Box[*Ts = "Protocol"]: ...
