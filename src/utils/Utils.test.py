import unittest
import pandas as pd
import sys

sys.path.append("/src/utils")
from utils.Utils import Utils


class TestUtils(unittest.TestCase):

    def test_normalizeTime(self):
        data = pd.DataFrame(
            {0: [1000000000, 2000000000, 3000000000], 1: [0.0, 0.1, 0.2]}
        )
        expected = pd.DataFrame({0: [0, 1, 2], 1: [0.0, 0.1, 0.2]})

        # Compare the DataFrames
        pd.testing.assert_frame_equal(Utils.normalizeTime(data), expected)


if __name__ == "__main__":
    unittest.main()
