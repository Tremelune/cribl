import unittest

import disk_reader


# Handy doc for unicode tests: https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
class TestDir(unittest.TestCase):
    def testReverseRead(self):
        # Note the unicode
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("lines.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_noNewline(self):
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("lines_no_newline.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_unicode(self):
        # Note the unicode
        expected = ["line b", "line "]
        actual = []
        for line in disk_reader.reverseRead("lines_unicode.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
