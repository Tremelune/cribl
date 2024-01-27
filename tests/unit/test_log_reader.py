import unittest
from unittest import mock

import log_reader


class TestDir(unittest.TestCase):
    def test_readLogs_badFilename(self):
        self.assertRaises(Exception, log_reader.readLogs, None)
        self.assertRaises(Exception, log_reader.readLogs, "../secrets.txt")

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs(self, mock_read):
        mock_read.return_value = iter(["wednesday 3a", "tuesday 9p"])

        res = log_reader.readLogs("blah", 99)
        lines = list(res)
        self.assertEqual(len(lines), 2)
        self.assertEqual("wednesday 3a", lines[0])
        self.assertEqual("tuesday 9p", lines[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_limit(self, mock_read):
        mock_read.return_value = ["wednesday 3a", "tuesday 9p", "monday 2p"]

        res = log_reader.readLogs("blah", 2)
        lines = list(res)
        self.assertEqual(len(lines), 2)
        self.assertEqual("wednesday 3a", lines[0])
        self.assertEqual("tuesday 9p", lines[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_filtering(self, mock_read):
        mock_read.return_value = [
            "one dog",
            "",
            "one cat",
            "all dogs go to heaven",
        ]

        res = log_reader.readLogs("blah", 100, "dog")
        lines = list(res)
        self.assertEqual(len(lines), 2)
        self.assertEqual("one dog", lines[0])
        self.assertEqual("all dogs go to heaven", lines[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_includeBlankLines(self, mock_read):
        mock_read.return_value = ["wednesday 3a", ""]

        res = log_reader.readLogs("blah", 99)
        lines = list(res)
        self.assertEqual(len(lines), 2)
        self.assertEqual("", lines[1])


if __name__ == '__main__':
    unittest.main()
