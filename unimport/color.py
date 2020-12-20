import sys
from typing import Tuple

__all__ = [
    "paint",
    "difference",
    "RESET",
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BOLD_WHITE",
]

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
        GetConsoleMode.errcheck = bool_errcheck

        SetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, DWORD)(
            ("SetConsoleMode", windll.kernel32),
            ((1, "hConsoleHandle"), (1, "dwMode")),
        )
        SetConsoleMode.errcheck = bool_errcheck

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


def paint(content: str, color: str) -> str:
    if TERMINAL_SUPPORT_COLOR:
        return color + content + RESET
    else:
        return content


def difference(content: Tuple[str, ...]) -> str:  # pragma: no cover
    lines = list(content)
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
