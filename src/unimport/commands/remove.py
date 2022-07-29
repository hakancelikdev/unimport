from pathlib import Path

from unimport.color import CYAN, GREEN, paint

__all__ = ("remove", "requirements_remove")


def remove(
    path: Path, encoding, newline, refactor_result: str, use_color
) -> None:
    with open(path, mode="w", encoding=encoding, newline=newline) as py_file:
        py_file.write(refactor_result)

    print(f"Refactoring '{paint(str(path), GREEN, use_color)}'")


def requirements_remove(
    path: Path, refactor_result: str, use_color: bool
) -> None:
    path.write_text(refactor_result)
    print(f"Refactoring '{paint(path.as_posix(), CYAN, use_color)}'")
