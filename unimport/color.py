import argparse
import sys
from typing import Tuple

__all__ = (
    "BLACK",
    "BLUE",
    "BOLD_WHITE",
    "COLOR_CHOICES",
    "CYAN",
    "GREEN",
    "MAGENTA",
    "RED",
    "RESET",
    "TERMINAL_SUPPORT_COLOR",
    "WHITE",
    "YELLOW",
    "add_color_option",
    "difference",
    "paint",
    "use_color",
)

if sys.platform == "win32":  # pragma: no cover (windows)

    def _enable() -> None:
        from ctypes import POINTER, WINFUNCTYPE, WinError, windll
        from ctypes.wintypes import BOOL, DWORD, HANDLE

        STD_ERROR_HANDLE = -12
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 4

        def bool_errcheck(result, func, args):
            if not result:
                raise WinError()
            return args

        GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(
            ("GetStdHandle", windll.kernel32),
            ((1, "nStdHandle"),),
        )

        GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(
            ("GetConsoleMode", windll.kernel32),
            ((1, "hConsoleHandle"), (2, "lpMode")),
        )
        GetConsoleMode.errcheck = (  # type: ignore[assignment, misc]
            bool_errcheck  # type: ignore[assignment]
        )

        SetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, DWORD)(
            ("SetConsoleMode", windll.kernel32),
            ((1, "hConsoleHandle"), (1, "dwMode")),
        )
        SetConsoleMode.errcheck = (  # type: ignore[assignment, misc]
            bool_errcheck  # type: ignore[assignment]
        )

        # As of Windows 10, the Windows console supports (some) ANSI escape
        # sequences, but it needs to be enabled using `SetConsoleMode` first.
        #
        # More info on the escape sequences supported:
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt638032(v=vs.85).aspx
        stderr = GetStdHandle(STD_ERROR_HANDLE)
        flags = GetConsoleMode(stderr)
        SetConsoleMode(stderr, flags | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

    try:
        _enable()
    except OSError:
        TERMINAL_SUPPORT_COLOR = False
    else:
        TERMINAL_SUPPORT_COLOR = True
else:  # pragma: win32 no cover
    TERMINAL_SUPPORT_COLOR = True

RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[97m"
BOLD_WHITE = "\033[1;37m"

COLOR_CHOICES = ("auto", "always", "never")


def paint(text: str, color: str, use_color_setting: bool = True) -> str:
    if use_color_setting:
        return color + text + RESET
    else:
        return text


def use_color(setting: str) -> bool:
    if setting not in COLOR_CHOICES:
        raise ValueError(setting)

    return setting == "always" or (
        setting == "auto" and sys.stderr.isatty() and TERMINAL_SUPPORT_COLOR
    )


def add_color_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--color",
        default="auto",
        type=use_color,
        metavar="{" + ",".join(COLOR_CHOICES) + "}",
        help="Select whether to use color in the output. Defaults to `%(default)s`.",
    )


def difference(text: Tuple[str, ...]) -> str:  # pragma: no cover
    lines = list(text)
    for i, line in enumerate(lines):
        if line.startswith("+++") or line.startswith("---"):
            lines[i] = paint(line, BOLD_WHITE)
        elif line.startswith("@@"):
            lines[i] = paint(line, CYAN)
        elif line.startswith("+"):
            lines[i] = paint(line, GREEN)
        elif line.startswith("-"):
            lines[i] = paint(line, RED)
    return "\n".join(lines)
