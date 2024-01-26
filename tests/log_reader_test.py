import unittest
import log_reader


class TestDir(unittest.TestCase):
    def test_filterLine(self):
        line = "puttin on the dog"
        self.assertEqual(line, log_reader._filterLine(line, "dog"))

        line = "love that doghouse livin"
        self.assertEqual(line, log_reader._filterLine(line, "dog"))

        line = "what's updog? nothing what's up with you"
        self.assertEqual(line, log_reader._filterLine(line, "dog"))

        line = "there's a snake in my boot!"
        self.assertIsNone(log_reader._filterLine(line, "dog"))

        line = "there's a snake in my boot!"
        self.assertEqual(line, log_reader._filterLine(line, ""))


if __name__ == '__main__':
    unittest.main()
