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

        expected = pd.DataFrame({0: [0, 1, 2], 1: [0.0, 0.1, 0.2]})

        data[0] = Utils.getNormalizedTime(data[0])

        print(data)

        # Compare the DataFrames
        pd.testing.assert_frame_equal(data, expected)


if __name__ == "__main__":
    unittest.main()
