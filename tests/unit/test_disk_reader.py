import unittest

import disk_reader


# Handy doc for unicode tests: https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
#
# Note that these will fail unless run from the "top" test directory. File paths are
# relatvie to where the test runner starts, and I'm not sure how to get both scenarios
# to work.
class TestDir(unittest.TestCase):
    def testReverseRead(self):
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("unit/lines.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_noNewline(self):
        expected = ["line e", "line d", "line c", "line b", "line a"]
        actual = []
        for line in disk_reader.reverseRead("unit/lines_no_newline.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)

    def testReverseRead_unicode(self):
        expected = ["line b", "line "]
        actual = []
        for line in disk_reader.reverseRead("unit/lines_unicode.txt"):
            actual.append(line)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
