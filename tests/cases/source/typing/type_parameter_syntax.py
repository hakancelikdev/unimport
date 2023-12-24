# pytest.mark.skipif(not PY312_PLUS, reason: "type parameter syntax is supported above python 3.12")

import x
import y

type Point = tuple[x, float]
