import unittest

import disk_reader
import log_reader


class TestDir(unittest.TestCase):
    def test_reverseRead(self):
        indexes = {0: "c", 1: "b", 2: "a"}
        i = 0
        for line in  disk_reader.reverseRead("lines.txt"):
            char = indexes[i]
            self.assertEqual(f"line {char}", line)
            i += 1
        self.assertEqual(3, i)

    def test_reverseRead_noNewline(self):
        indexes = {0: "c", 1: "b", 2: "a"}
        i = 0
        for line in  disk_reader.reverseRead("lines_no_newline.txt"):
            char = indexes[i]
            self.assertEqual(f"line {char}", line)
            i += 1
        self.assertEqual(3, i)


if __name__ == '__main__':
    unittest.main()
