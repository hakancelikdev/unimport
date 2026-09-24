import functools
import re
from typing import cast

from unimport import typing as T

__all__ = ("generic_visit", "is_skip_comment", "skip_import")


def generic_visit(func: T.FunctionT) -> T.FunctionT:
    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):
        func(self, node, *args, **kwargs)
        self.generic_visit(node)

    return cast(T.FunctionT, wrapper)


UNUSED_IMPORT_NOQA_CODE = "F401"  # the flake8 / ruff code for unused imports

SKIP_IMPORT_COMMENT_REGEX = re.compile(r"unimport: {0,1}skip", re.IGNORECASE)
NOQA_COMMENT_REGEX = re.compile(r"\bnoqa\b(?::\s*(?P<codes>[A-Z0-9]+(?:[,\s]+[A-Z0-9]+)*))?", re.IGNORECASE)


def is_skip_comment(source_segment: str) -> bool:
    """Whether the comments of an import statement skip it.

    ``# unimport: skip``, a bare ``# noqa`` and ``# noqa: F401`` do;
    ``# noqa`` for other codes (e.g. ``# noqa: E501``) does not.
    """
    for comment in re.findall(r"#.*", source_segment):
        if SKIP_IMPORT_COMMENT_REGEX.search(comment):
            return True
        if match := NOQA_COMMENT_REGEX.search(comment):
            codes = match.group("codes")
            if codes is None or UNUSED_IMPORT_NOQA_CODE in re.split(r"[,\s]+", codes.upper()):
                return True
    return False


def skip_import(func: T.FunctionT) -> T.FunctionT:
    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):
        source_segment = "\n".join(self.source.splitlines()[node.lineno - 1 : node.end_lineno])
        skip_comment = is_skip_comment(source_segment)
        if not any((skip_comment, self.any_import_error)):
            func(self, node, *args, **kwargs)

    return cast(T.FunctionT, wrapper)
