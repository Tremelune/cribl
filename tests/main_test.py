import unittest

import main


class TestDir(unittest.TestCase):
    def test_doStuff(self):
        res = main.doStuff()
        self.assertEqual("oh noes", res)


if __name__ == '__main__':
    unittest.main()
