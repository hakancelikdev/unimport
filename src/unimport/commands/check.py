from pathlib import Path
from typing import List, Union

from unimport.color import CYAN, GREEN, RED, YELLOW, paint
from unimport.statement import Import, ImportFrom

__all__ = ("check", "requirements_check")


def check(
    path: Path,
    unused_imports: List[Union[Import, ImportFrom]],
    use_color_setting: bool,
) -> None:
    for imp in unused_imports:
        if isinstance(imp, ImportFrom) and imp.star and imp.suggestions:
            context = (
                paint(f"from {imp.name} import *", RED, use_color_setting)
                + " -> "
                + paint(
                    f"from {imp.name} import {', '.join(imp.suggestions)}",
                    GREEN,
                    use_color_setting,
                )
            )
        else:
            context = paint(imp.name, YELLOW, use_color_setting)
        print(
            context
            + " at "
            + paint(path.as_posix(), GREEN, use_color_setting)
            + ":"
            + paint(str(imp.lineno), GREEN, use_color_setting)
        )


def requirements_check(
    path: Path, index: int, requirement: str, use_color_setting: bool
) -> None:
    print(
        f"{paint(requirement, CYAN, use_color_setting)} at "
        f"{paint(path.as_posix(), CYAN, use_color_setting)}:{paint(str(index + 1), CYAN, use_color_setting)}"
    )
