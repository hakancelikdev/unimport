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


class Color:
    reset = "\033[0m"

    def __init__(self, content: str) -> None:
        for name, code in COLORS.items():
            setattr(self, name, code + content + self.reset)
