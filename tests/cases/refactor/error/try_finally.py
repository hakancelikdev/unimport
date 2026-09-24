try:
    pass
finally:
    pass

try:
    try:
        pass
    finally:
        pass
    import ujson as json
except ImportError:
    import json

print(json)
