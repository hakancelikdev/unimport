from pathlib import Path

from unimport import utils
from unimport.color import paint
from unimport.enums import Color

__all__ = ("permission",)


def permission(
    path: Path,
    encoding: str,
    newline: str,
    refactor_result: str,
    use_color: bool,
) -> None:
    action = input(f"Apply suggested changes to '{paint(str(path), Color.YELLOW, use_color)}' [Y/n/q] ? >").lower()
    if action == "q":
        raise SystemExit(1)
    elif utils.action_to_bool(action):
        from unimport import commands

        commands.remove(path, encoding, newline, refactor_result, use_color)
