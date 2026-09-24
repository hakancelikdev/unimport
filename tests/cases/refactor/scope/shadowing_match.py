# pytest.mark.skipif(not PY310_PLUS, reason: "match statement is supported above python 3.10")



def f(value):
    match value:
        case [os, *rest]:
            return os, rest
        case {"key": 1, **sys}:
            return sys
