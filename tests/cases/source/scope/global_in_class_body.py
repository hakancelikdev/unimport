import json


def f():
    json = None

    class A:
        global json
        x = json.dumps(1)

    return A
