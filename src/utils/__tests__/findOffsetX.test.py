from pathlib import Path
import unittest
import pandas as pd
import sys


# this is ugly and not very robust
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "utils"))

from findOffsetX import findOffsetX


class TestFindOffsetX(unittest.TestCase):

    def test_positiveOffset(self):

        signal = pd.Series([1, 2, 3, 4, 5, 0, 0, 0, 0, 0])
        reference = pd.Series([0, 0, 1, 2, 3, 4, 5])

        offset = findOffsetX(signal, reference)

        print("Offset: ", offset)

        self.assertEqual(offset, 2)


if __name__ == "__main__":
    unittest.main()
