import unittest
import log_reader


# Note that the files this tests against are always changing, so the tests will fail
# sometimes without changes. Not the best tests, but better than writing random files
# to disk for this...If they were long-lived I'd worry about it.
class TestDir(unittest.TestCase):
    def test_readLogs_filename(self):
        res = log_reader.readLogs("system.log", 2)
        self.assertTrue("__thr_AMMuxedDeviceDisconnected" in res[0])
        self.assertFalse("rdisk5s1" in res[0])

        res = log_reader.readLogs("fsck_apfs.log", 2)  # Blank line at EOF
        self.assertTrue("rdisk5s1" in res[1])
        self.assertFalse("__thr_AMMuxedDeviceDisconnected" in res[0])

    def test_readLogs_filter(self):
        res = log_reader.readLogs("system.log", 1, "syslogd")
        self.assertTrue("ASL Sender Statistics" in res[0])

    def test_readLogs_bigBoy(self):
        res = log_reader.readLogs("bigboy.log", 100)
        self.assertEqual(100, len(res))
        self.assertEqual("067456160 This is line 67456160", res[0])


if __name__ == '__main__':
    unittest.main()
