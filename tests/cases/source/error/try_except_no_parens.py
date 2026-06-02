# pytest.mark.skipif(not PY314_PLUS, reason: "except without parens (PEP 758) is supported above python 3.14")

# https://github.com/hakancelikdev/unimport/issues/326

import os

try:
    pass
except ValueError, TypeError:
    pass

try:
    pass
except ValueError, TypeError, KeyError:
    pass
