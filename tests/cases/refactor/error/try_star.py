# pytest.mark.skipif(not PY311_PLUS, reason: "except* is supported above python 3.11")

try:
    import ujson as json
except* ImportError:
    import json

print(json)
