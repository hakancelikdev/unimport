import sys
from typing import TYPE_CHECKING, Any

if sys.version_info < (3, 7):
    if TYPE_CHECKING:

        class ForwardRef:
            def __init__(self, arg: Any):
                pass

            def _eval_type(self, globalns: Any, localns: Any) -> Any:
                pass

    else:
        from typing import _ForwardRef as ForwardRef
else:
    from typing import ForwardRef

print(ForwardRef)
