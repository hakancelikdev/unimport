import unittest

from tests.analyzer.utils import AnalyzerTestCase
from unimport.constants import PY38_PLUS
from unimport.statement import ImportFrom, Name


@unittest.skipIf(
    not PY38_PLUS, "This feature is only available for python 3.8."
)
class TypeCommentsTestCase(AnalyzerTestCase):
    def test_type_comments(self):
        self.assertUnimportEqual(
            source="""\
            from typing import Any
            from typing import Tuple
            from typing import Union
            def function(a, b):
                # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
                pass
            """,
            expected_names=[
                Name(lineno=4, name="Any"),
                Name(lineno=4, name="str"),
                Name(lineno=4, name="Union"),
                Name(lineno=4, name="Tuple"),
                Name(lineno=4, name="Tuple"),
                Name(lineno=4, name="str"),
                Name(lineno=4, name="str"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="Any",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=2,
                    column=1,
                    name="Tuple",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="Union",
                    package="typing",
                    star=False,
                    suggestions=[],
                ),
            ],
        )
