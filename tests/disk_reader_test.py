import unittest

import disk_reader


# Handy doc for unicode tests: https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
class TestDir(unittest.TestCase):
    def testReverseRead(self):
        # Note the unicode
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("lines.txt", 0, 100):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_noNewline(self):
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("lines_no_newline.txt", 0, 100):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_limit(self):
        expected = ["line e", "line d"]
        actual = []
        for line in disk_reader.reverseRead("lines.txt", 0, 2):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_limit(self):
        expected = ["line e", "line d"]
        actual = []
        for line in disk_reader.reverseRead("lines_no_newline.txt", 0, 2):
            actual.append(line)
        self.assertEqual(expected, actual)

    def test_reverseRead_limitOffsetNoNewline(self):
        return None

    def testReverseRead_unicode(self):
        # Note the unicode
        expected = ["line b", "line "]
        actual = []
        for line in disk_reader.reverseRead("lines_unicode.txt", 0, 100):
            actual.append(line)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
