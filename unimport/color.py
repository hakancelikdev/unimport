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
        self.content = content

    def template(self, color: str) -> str:
        return COLORS[color] + self.content + self.reset

    def __getattribute__(self, name: str) -> str:
        if name in COLORS:
            return self.template(name)
        return super().__getattribute__(name)
