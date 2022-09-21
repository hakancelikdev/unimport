from pathlib import Path

from unimport.color import paint
from unimport.enums import Color

__all__ = ("remove",)


def remove(path: Path, encoding, newline, refactor_result: str, use_color) -> None:
    with open(path, mode="w", encoding=encoding, newline=newline) as py_file:
        py_file.write(refactor_result)

    print(f"Refactoring '{paint(str(path), Color.GREEN, use_color)}'")
