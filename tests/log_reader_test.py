import unittest
from unittest import mock

import log_reader


class TestDir(unittest.TestCase):
    def test_readLogs_badFilename(self):
        self.assertRaises(Exception, log_reader.readLogs, None)

    def test_readLogs_badLimit(self):
        self.assertRaises(Exception, log_reader.readLogs, "filename.txt", 1000)

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs(self, mock_read):
        mock_read.return_value = ["wednesday 3a", "tuesday 9p",]

        res = log_reader.readLogs("blah")
        self.assertEqual(len(res), 2)
        self.assertEqual("wednesday 3a", res[0])
        self.assertEqual("tuesday 9p", res[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_limit(self, mock_read):
        mock_read.return_value = [
            "wednesday 3a",
            "tuesday 9p",
            "monday 2p",
        ]

        res = log_reader.readLogs("blah", 2)
        self.assertEqual(len(res), 2)
        self.assertEqual("wednesday 3a", res[0])
        self.assertEqual("tuesday 9p", res[1])

    @mock.patch("disk_reader.reverseRead")
    def test_readLogs_includeBlankLines(self, mock_read):
        mock_read.return_value = [
            "wednesday 3a",
            "",
        ]

        res = log_reader.readLogs("blah")
        self.assertEqual(len(res), 2)
        self.assertEqual("", res[1])

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
