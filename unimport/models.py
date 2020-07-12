from typing import List, TYPE_CHECKING, Optional
from types import ModuleType

if TYPE_CHECKING:
    from typing_extensions import TypedDict

    class TYPE_NAME(TypedDict):
        lineno: int
        name: str

    class TYPE_IMPORT(TypedDict):
        lineno: int
        name: str
        star: bool
        module: Optional[ModuleType]
        modules: List[str]

