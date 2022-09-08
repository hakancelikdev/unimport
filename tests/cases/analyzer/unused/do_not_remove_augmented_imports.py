from typing import List, Union

from unimport.statement import Import, ImportFrom, Name

__all__ = ["NAMES", "IMPORTS", "UNUSED_IMPORTS"]


NAMES: List[Name] = [Name(lineno=4, name="AUTHENTICATION_BACKENDS", is_all=False)]
IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=1,
        name="AUTHENTICATION_BACKENDS",
        package="django.conf.global_settings",
        star=False,
        suggestions=[],
    ),
    ImportFrom(
        lineno=1,
        column=2,
        name="TEMPLATE_CONTEXT_PROCESSORS",
        package="django.conf.global_settings",
        star=False,
        suggestions=[],
    ),
]
UNUSED_IMPORTS: List[Union[Import, ImportFrom]] = [
    ImportFrom(
        lineno=1,
        column=2,
        name="TEMPLATE_CONTEXT_PROCESSORS",
        package="django.conf.global_settings",
        star=False,
        suggestions=[],
    )
]
