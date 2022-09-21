import functools
import re
from typing import cast

from unimport import constants as C
from unimport import typing as T

__all__ = ("generic_visit", "skip_import")


def generic_visit(func: T.FunctionT) -> T.FunctionT:
    """decorator to make visitor work _generic_visit."""

    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):

        func(self, node, *args, **kwargs)
        self.generic_visit(node)

    return cast(T.FunctionT, wrapper)


def skip_import(func: T.FunctionT) -> T.FunctionT:
    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):
        if C.PY38_PLUS:
            source_segment = "\n".join(self.source.splitlines()[node.lineno - 1: node.end_lineno])
        else:
            source_segment = self.source.splitlines()[node.lineno - 1]

        skip_comment = bool(re.search(self.skip_import_comments_regex, source_segment, re.IGNORECASE))
        if not any((skip_comment, self.any_import_error)):
            func(self, node, *args, **kwargs)

    return cast(T.FunctionT, wrapper)
