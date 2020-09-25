import sys

COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[97m",
    "bold_white": "\033[1;37m",
}


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
            ("GetStdHandle", windll.kernel32), ((1, "nStdHandle"),),
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
        terminal_supports_color = False
    else:
        terminal_supports_color = True
else:  # pragma: win32 no cover
    terminal_supports_color = True


class Color:
    reset = "\033[0m"

    def __init__(self, content: str) -> None:
        self.content = content

    def template(self, color: str) -> str:
        if terminal_supports_color:
            return COLORS[color] + self.content + self.reset
        else:
            return self.content

    def __getattribute__(self, name: str) -> str:
        if name in COLORS:
            return self.template(name)
        return super().__getattribute__(name)
