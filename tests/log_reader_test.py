import unittest
import log_reader


class TestDir(unittest.TestCase):
    def test_doStuff(self):
        res = log_reader.readLogs("system.log", 1)
        self.assertTrue("AMPDeviceDiscoveryAgent" in res)


if __name__ == '__main__':
    unittest.main()
