from pathlib import Path
from typing import List, Union

from unimport.color import paint
from unimport.enums import Color
from unimport.statement import Import, ImportFrom

__all__ = ("check",)


def check(path: Path, unused_imports: List[Union[Import, ImportFrom]], use_color: bool) -> None:
    for imp in unused_imports:
        if isinstance(imp, ImportFrom) and imp.star and imp.suggestions:
            context = (
                paint(f"from {imp.name} import *", Color.RED, use_color)
                + " -> "
                + paint(
                    f"from {imp.name} import {', '.join(imp.suggestions)}",
                    Color.GREEN,
                    use_color,
                )
            )
        else:
            context = paint(imp.name, Color.YELLOW, use_color)
        print(
            context
            + " at "
            + paint(path.as_posix(), Color.GREEN, use_color)
            + ":"
            + paint(str(imp.lineno), Color.GREEN, use_color)
        )
