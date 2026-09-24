import sys

if sys.version_info >= (3, 8):
    if sys.platform == "win32":
        pass
    from typing import Literal
else:
    from typing_extensions import Literal

print(Literal)
