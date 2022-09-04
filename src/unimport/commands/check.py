from pathlib import Path
from typing import List, Union

from unimport.color import GREEN, RED, YELLOW, paint
from unimport.statement import Import, ImportFrom

__all__ = ("check",)


def check(
    path: Path,
    unused_imports: List[Union[Import, ImportFrom]],
    use_color: bool,
) -> None:
    for imp in unused_imports:
        if isinstance(imp, ImportFrom) and imp.star and imp.suggestions:
            context = (
                paint(f"from {imp.name} import *", RED, use_color)
                + " -> "
                + paint(
                    f"from {imp.name} import {', '.join(imp.suggestions)}",
                    GREEN,
                    use_color,
                )
            )
        else:
            context = paint(imp.name, YELLOW, use_color)
        print(
            context
            + " at "
            + paint(path.as_posix(), GREEN, use_color)
            + ":"
            + paint(str(imp.lineno), GREEN, use_color)
        )
