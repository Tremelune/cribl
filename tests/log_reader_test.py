import unittest
import log_reader


class TestDir(unittest.TestCase):
    # This test will fail on any other machine. Might could pass in a mock disk_reader,
    # but let's get this done first...
    def test_doStuff(self):
        res = log_reader.readLogs("system.log", 1)
        self.assertTrue("__thr_AMMuxedDeviceDisconnected" in res[0])
        self.assertFalse("rdisk5s1" in res[0])

        res = log_reader.readLogs("fsck_apfs.log", 1)
        self.assertTrue("rdisk5s1" in res[0])
        self.assertFalse("__thr_AMMuxedDeviceDisconnected" in res[0])


if __name__ == '__main__':
    unittest.main()
