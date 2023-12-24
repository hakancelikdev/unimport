# pytest.mark.skipif(not PY312_PLUS, reason: "type parameter syntax is supported above python 3.12")

import x

type Point = tuple[x, float]
