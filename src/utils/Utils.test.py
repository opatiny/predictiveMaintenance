import unittest
import pandas as pd
import sys

sys.path.append("/src/utils")

import Utils


class TestUtils(unittest.TestCase):

    def test_normalizeTime(self):
        data = pd.DataFrame({0: [10000000, 20000000, 30000000], 1: [0.0, 0.1, 0.2]})

        expected = pd.DataFrame({0: [0.0, 1.0, 2.0], 1: [0.0, 0.1, 0.2]})

        data[0] = Utils.getNormalizedTime(data[0])

        # Compare the DataFrames
        pd.testing.assert_frame_equal(data, expected)

    def test_getDate(self):
        timestamp = 133830456135230000

        expected = "2025-02-03 08:40:13"

        date = Utils.getDate(timestamp)

        self.assertEqual(date, expected)

    def test_removeDuplicates(self):
        data = pd.DataFrame(
            {
                "timestamp": [10000000, 20000000, 20000000, 30000000],
                1: [0.0, 0.1, 0.1, 0.2],
            }
        )

        expected = pd.DataFrame(
            {"timestamp": [10000000, 20000000, 30000000], 1: [0.0, 0.1, 0.2]}
        )

        data = Utils.removeDuplicates(data, True)
        # reset index
        data = data.reset_index(drop=True)

        # Compare the DataFrames
        pd.testing.assert_frame_equal(data, expected)

    def test_normalizeSignal(self):
        data = pd.Series([-2, -1, 0.0, 1.0, 2.0])

        expected = pd.Series([-1.0, -0.5, 0.0, 0.5, 1.0])

        data = Utils.normalizeSignal(data)

        # Compare the Series
        pd.testing.assert_series_equal(data, expected)


if __name__ == "__main__":
    unittest.main()
