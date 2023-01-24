from pathlib import Path

from unimport import utils
from unimport.color import paint
from unimport.enums import Color

__all__ = ("permission",)


def permission(path: Path, use_color: bool) -> bool:
    action = input(f"Apply suggested changes to '{paint(str(path), Color.YELLOW, use_color)}' [Y/n/q] ? >").lower()
    if action == "q":
        raise SystemExit(1)
    return utils.action_to_bool(action)
