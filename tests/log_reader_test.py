import unittest
from unittest import mock

import log_reader


class TestDir(unittest.TestCase):
    def test_readLogs_badFilename(self):
        self.assertRaises(Exception, log_reader.readLogs, None)
        self.assertRaises(Exception, log_reader.readLogs, "../secrets.txt")

    def test_readLogs_badLimit(self):
        self.assertRaises(Exception, log_reader.readLogs, "filename.txt", 1000)
        self.assertRaises(Exception, log_reader.readLogs, "filename.txt", 0)

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs(self, mock_read):
        mock_read.return_value = ["wednesday 3a", "tuesday 9p"]

        res = log_reader.readLogs("blah")
        self.assertEqual(len(res), 2)
        self.assertEqual("wednesday 3a", res[0])
        self.assertEqual("tuesday 9p", res[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_limit(self, mock_read):
        mock_read.return_value = ["wednesday 3a", "tuesday 9p", "monday 2p"]

        res = log_reader.readLogs("blah", 2)
        self.assertEqual(len(res), 2)
        self.assertEqual("wednesday 3a", res[0])
        self.assertEqual("tuesday 9p", res[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_filtering(self, mock_read):
        mock_read.return_value = [
            "one dog",
            "",
            "one cat",
            "all dogs go to heaven",
        ]

        res = log_reader.readLogs("blah", 100, "dog")
        self.assertEqual(len(res), 2)
        self.assertEqual("one dog", res[0])
        self.assertEqual("all dogs go to heaven", res[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_includeBlankLines(self, mock_read):
        mock_read.return_value = ["wednesday 3a", ""]

        res = log_reader.readLogs("blah")
        self.assertEqual(len(res), 2)
        self.assertEqual("", res[1])

    def test_filterLine(self):
        lines = []
        line = "puttin on the dog"
        log_reader._addFilteredLine(lines, line, "dog")
        self.assertEqual(line, lines[0])

        lines = []
        line = "love that doghouse livin"
        log_reader._addFilteredLine(lines, line, "dog")
        self.assertEqual(line, lines[0])

        lines = []
        line = "what's updog? nothing what's up with you"
        log_reader._addFilteredLine(lines, line, "dog")
        self.assertEqual(line, lines[0])

        lines = []
        line = "there's a snake in my boot!"
        log_reader._addFilteredLine(lines, line, "dog")
        self.assertEqual(0, len(lines))

        lines = []
        line = "there's a snake in my boot!"
        log_reader._addFilteredLine(lines, line, "")
        self.assertEqual(line, lines[0])


if __name__ == '__main__':
    unittest.main()
