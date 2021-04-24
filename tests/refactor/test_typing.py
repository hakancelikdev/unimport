import unittest

from tests.refactor.utils import RefactorTestCase
from unimport.constants import PY38_PLUS


class TypingTestCase(RefactorTestCase):

    include_star_import = True

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comments(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Any
            from typing import Tuple
            from typing import Union
            def function(a, b):
                # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
                pass
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comments_with_variable(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            test_variable = [2] # type: List[int]
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comment_params(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            def x(
               f: # type:List,
               r: # type:str
            ):
               pass
            """
        )

    @unittest.skipIf(
        not PY38_PLUS, "This feature is only available for python 3.8."
    )
    def test_type_comment_funcdef(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import List
            def x(y):
               # type: (str) -> List[str]
               pass
            """
        )

    def test_variable(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            test: "List[Dict]"
            """
        )

    def test_function_arg(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            def test(arg:"List[Dict]") -> None:
               pass
            """
        )

    def test_function_str_arg(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, Literal
            def test(item, when: "Literal['Dict']") -> None:
               pas
            """
        )

    def test_function_return(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from typing import Dict, List
            def test(arg: list) -> "List[Dict]":
               pass
            """
        )
