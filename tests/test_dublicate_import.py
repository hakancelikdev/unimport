import unittest
from unimport.session import Session

# These imports to write in modules below.
from pathlib import Path
class TestDublicate(unittest.TestCase):

	def setUp(self):
		self.session = Session()

	def test_full_unused(self):
		source = (
			"from x import y\n"
			"from x import y\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'y', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'y', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_one_unused(self):
		source = (
			"from patlib import Path\n"
			"from patlib import Path\n"
			"from patlib import Path\n"
			"Path"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'Path', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'Path', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_full_dublicate_unused(self):
		source = (
			"from patlib import Path\n"
			"from patlib import Path\n"
			"from t import r\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'Path', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'Path', 'star': False
				},
				{
					'lineno': 3, 'module': None, 'name': 'r', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)


	def test_different_dublicate_unused(self):
		source = (
			"from x import z\n"
			"from y import z\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'z', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'z', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_different_dublicate_used(self):
		source = (
			"from x import z\n"
			"from y import z\n"
			"print(z)\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'z', 'star': False
				},
			], list(self.session.scanner.get_unused_imports())
		)
