import json


def f():
    json = None

    def g():
        global json

        def h():
            return json.dumps(1)

        return h

    return g
