from pathlib import Path

from unimport import utils
from unimport.color import difference

__all__ = ("diff",)


def diff(path: Path, source: str, refactor_result: str, use_color: bool = True) -> bool:
    diff_ = utils.diff(source=source, refactor_result=refactor_result, fromfile=path)
    exists_diff = bool(diff_)
    if exists_diff:
        print(difference(diff_, use_color))

    return exists_diff
