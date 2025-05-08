import unittest
import pandas as pd
import sys

sys.path.append("/src/utils")

from findCommonSection import findCommonSection


class TestFindCommonSection(unittest.TestCase):

    def test_positiveOffset(self):
        reference = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9])
        signal = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        offset = 2

        result = findCommonSection(signal, reference, offset)

        expected = pd.DataFrame(
            {
                "signal": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                ],
                "reference": [3, 4, 5, 6, 7, 8, 9],
            }
        )

        pd.testing.assert_frame_equal(result, expected)

    def test_positiveOffset(self):
        reference = pd.Series([1, 2, 3, 4, 5, 6, 7, 8])
        signal = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        offset = -3

        result = findCommonSection(signal, reference, offset)

        expected = pd.DataFrame(
            {
                "signal": [4, 5, 6, 7, 8, 9, 10],
                "reference": [1, 2, 3, 4, 5, 6, 7],
            }
        )

        # Compare the DataFrames
        pd.testing.assert_frame_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
