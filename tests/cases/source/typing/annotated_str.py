from typing import Annotated

from foo import Bar, doc


x: Annotated["Bar", "doc"] = None
