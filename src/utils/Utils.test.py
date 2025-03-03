import unittest
import pandas as pd

import Utils


class TestUtils(unittest.TestCase):
    def testTests(self):
        self.assertEqual(1, 10)

    def test_normalizeTime(self):
        data = pd.DataFrame(
            {0: [1000000000, 2000000000, 3000000000], 1: [0.0, 0.1, 0.2]}
        )
        self.assertEqual("foo".upper(), "FOO")


if __name__ == "__main__":
    unittest.main()
