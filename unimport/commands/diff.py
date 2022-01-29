from pathlib import Path

from unimport import utils
from unimport.color import difference as color_difference

__all__ = ["diff", "requirements_diff"]


def diff(
    path: Path,
    source: str,
    refactor_result: str,
) -> bool:
    diff = utils.diff(
        source=source, refactor_result=refactor_result, fromfile=path
    )
    exists_diff = bool(diff)
    if exists_diff:
        print(color_difference(diff))

    return exists_diff


def requirements_diff(path: Path, source: str, refactor_result: str) -> bool:
    diff = utils.diff(
        source=source,
        refactor_result=refactor_result,
        fromfile=path,
    )
    exists_diff = bool(diff)
    if exists_diff:
        print(color_difference(diff))

    return exists_diff
