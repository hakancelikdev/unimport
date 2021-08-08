from tests.refactor.utils import RefactorTestCase


class StyleTestCase(RefactorTestCase):
    def test_global_import(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x

            def f():
                import x

                x

            """,
            """\

            def f():
                import x

                x

            """,
        )

    def test_nonlocal_import(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x

            def func():
                import x

                def inner():
                    import x
                    x

            """,
            """\

            def func():

                def inner():
                    import x
                    x

            """,
        )

    def test_nonlocal_import_2(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x

            def func():
                import x

                def inner():
                    import x
                    x

                x

            """,
            """\

            def func():
                import x

                def inner():
                    import x
                    x

                x

            """,
        )

    def test_nonlocal_import_3(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            import x

            def func():
                import x

                def inner():
                    import x
                    x

                x

            x

            """
        )

    def test_nonlocal_import_4(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x

            def func():
                import x

                def inner():
                    import x
                    x

            """,
            """\

            def func():

                def inner():
                    import x
                    x

            """,
        )

    def test_nonlocal_import_5(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            import x

            def func():
                def inner():
                    x

            """
        )
