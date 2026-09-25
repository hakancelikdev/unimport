import json


def f():
    json = None

    def g():
        global json
        return json.dumps(1)

    return g
