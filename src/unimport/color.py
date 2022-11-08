import sys
from typing import Tuple

from unimport.enums import Color

__all__ = (
    "TERMINAL_SUPPORT_COLOR",
    "difference",
    "paint",
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


def paint(text: str, color: Color, use_color: bool = True) -> str:
    return color.value + text + Color.RESET.value if use_color else text


def difference(text: Tuple[str, ...], use_color: bool = True) -> str:  # pragma: no cover
    lines = list(text)
    for i, line in enumerate(lines):
        if line.startswith("+++") or line.startswith("---"):
            lines[i] = paint(line, Color.BOLD_WHITE, use_color)
        elif line.startswith("@@"):
            lines[i] = paint(line, Color.CYAN, use_color)
        elif line.startswith("+"):
            lines[i] = paint(line, Color.GREEN, use_color)
        elif line.startswith("-"):
            lines[i] = paint(line, Color.RED, use_color)
    return "\n".join(lines)
