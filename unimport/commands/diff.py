from pathlib import Path

from unimport import utils
from unimport.color import difference as color_difference

__all__ = ("diff",)


def diff(
    path: Path,
    source: str,
    refactor_result: str,
) -> bool:
    diff_ = utils.diff(
        source=source, refactor_result=refactor_result, fromfile=path
    )
    exists_diff = bool(diff_)
    if exists_diff:
        print(color_difference(diff_))

    return exists_diff
