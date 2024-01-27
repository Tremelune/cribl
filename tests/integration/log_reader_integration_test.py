import unittest
import log_reader


class TestDir(unittest.TestCase):
    def test_readLogs_filename(self):
        res = log_reader.readLogs("system.log", 1)
        self.assertTrue("__thr_AMMuxedDeviceDisconnected" in res[0])
        self.assertFalse("rdisk5s1" in res[0])

        res = log_reader.readLogs("fsck_apfs.log", 2)  # Blank line at EOF
        self.assertTrue("rdisk5s1" in res[1])
        self.assertFalse("__thr_AMMuxedDeviceDisconnected" in res[0])


if __name__ == '__main__':
    unittest.main()
