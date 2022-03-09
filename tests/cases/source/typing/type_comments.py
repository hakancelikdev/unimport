# skip; condition: not PY38_PLUS, reason: This feature is only available for python 3.8.

from typing import Any
from typing import Tuple
from typing import Union


def function(a, b):
    # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
    pass
