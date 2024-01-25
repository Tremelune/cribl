import unittest

import log_endpoint


class TestDir(unittest.TestCase):
    def test_doStuff(self):
        res = log_endpoint.get_log()
        # self.assertEqual("oh noes", res)
        self.assertTrue("moon" in res)


if __name__ == '__main__':
    unittest.main()
