import x
import x.y
import x.y.z
import x, x.y
import x, x.y, x.y.z
import x.y, x.y.z, x.y.z
import x.y, x.y, x.y.z
from x import y
from x import y, z
from x.y import z, q
from x.y.z import z, q, zq
some()
calls()
# and comments
def maybe_functions(): # type: ignore
    after()
from x import (
    y
)
from x import (
    y,
    z
)
from x import (
    y,
    z,
)
from x.y import (
    z,
    q,
    u,
)
from x.y import (
    z,
    q,
    u,
    z,
    q,
)
