from pathlib import Path

from unimport import utils
from unimport.color import CYAN, YELLOW, paint

__all__ = ("permission", "requirements_permission")


def permission(
    path: Path,
    encoding: str,
    newline: str,
    refactor_result: str,
    use_color_setting: bool,
) -> None:
    action = input(
        f"Apply suggested changes to '{paint(str(path), YELLOW, use_color_setting)}' [Y/n/q] ? >"
    ).lower()
    if action == "q":
        raise SystemExit(1)
    elif utils.actiontobool(action):
        from unimport.commands import remove

        remove(path, encoding, newline, refactor_result, use_color_setting)


def requirements_permission(
    path: Path, refactor_result: str, use_color_setting: bool
):
    action = input(
        f"Apply suggested changes to '{paint(path.as_posix(), CYAN, use_color_setting)}' [Y/n/q] ? >"
    ).lower()
    if action == "q":
        return 1
    if utils.actiontobool(action):
        from unimport.commands import requirements_remove

        requirements_remove(path, refactor_result, use_color_setting)
