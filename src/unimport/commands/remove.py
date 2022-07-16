from pathlib import Path

from unimport.color import CYAN, GREEN, paint

__all__ = ("remove", "requirements_remove")


def remove(
    path: Path, encoding, newline, refactor_result: str, use_color_setting
) -> None:
    with open(path, mode="w", encoding=encoding, newline=newline) as py_file:
        py_file.write(refactor_result)

    print(f"Refactoring '{paint(str(path), GREEN, use_color_setting)}'")


def requirements_remove(
    path: Path, refactor_result: str, use_color_setting: bool
) -> None:
    path.write_text(refactor_result)
    print(f"Refactoring '{paint(path.as_posix(), CYAN, use_color_setting)}'")
