from enum import Enum

__all__ = ("Emoji", "Color")


class Emoji(str, Enum):
    STAR = "\U0001F929"
    PARTYING_FACE = "\U0001F973"


class Color(str, Enum):
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
