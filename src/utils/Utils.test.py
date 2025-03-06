import unittest
import pandas as pd
import sys

sys.path.append("/src/utils")

import Utils


class TestUtils(unittest.TestCase):

    def test_normalizeTime(self):
        data = pd.DataFrame(
            {0: [1000000000, 2000000000, 3000000000], 1: [0.0, 0.1, 0.2]}
        )
        expected = [0, 1, 2]

        result = Utils.normalizeTime(data)

        print(result)

        # Compare the DataFrames
        pd.testing.assert_frame_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
