import enum

__all__ = ("Emoji", "Color", "ColorSelect")


class _StrEnum(str, enum.Enum):
    """A str enum that formats as its value, like enum.StrEnum (Python 3.11+).

    Since Python 3.12, format() of a plain ``str, Enum`` mixin returns
    ``Class.MEMBER``, so f-strings printed ``Emoji.STAR``.
    """

    def __str__(self) -> str:
        return self.value

    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)


class Emoji(_StrEnum):
    STAR = "\U0001f929"
    PARTYING_FACE = "\U0001f973"


class Color(_StrEnum):
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


class ColorSelect(_StrEnum):
    AUTO = "auto"
    ALWAYS = "always"
    NEVER = "never"
