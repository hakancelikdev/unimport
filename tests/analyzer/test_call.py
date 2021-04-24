from tests.analyzer.utils import AnalyzerTestCase
from unimport.statement import ImportFrom, Name


class CallTestCase(AnalyzerTestCase):
    def test_call_in_name(self):
        self.assertUnimportEqual(
            source="""\
            from pathlib import Path
            CURRENT_DIR = Path(__file__).parent
            """,
            expected_names=[
                Name(lineno=2, name="CURRENT_DIR"),
                Name(lineno=2, name="Path"),
                Name(lineno=2, name="__file__"),
            ],
            expected_imports=[
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="Path",
                    package="pathlib",
                    star=False,
                    suggestions=[],
                ),
            ],
        )

    def test_call_in_attr(self):
        self.assertUnimportEqual(
            source="""\
            a(b.c).d
            """,
            expected_names=[
                Name(lineno=1, name="a"),
                Name(lineno=1, name="b.c"),
            ],
        )

    def test_call_in_str_attr(self):
        self.assertUnimportEqual(
            source="""\
            a("b.c").d
            """,
            expected_names=[
                Name(lineno=1, name="a"),
            ],
        )

    def test_attr_in_call_in_attr(self):
        self.assertUnimportEqual(
            source="""\
            a.b(c.d).f
            """,
            expected_names=[
                Name(lineno=1, name="a.b"),
                Name(lineno=1, name="c.d"),
            ],
        )
