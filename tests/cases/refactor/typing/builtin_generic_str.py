from foo import Bar, Baz, Qux


x: list["Bar"] = []


def f(a: dict[str, "Baz"]) -> tuple["Qux", ...]: ...
