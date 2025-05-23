from pathlib import Path
import unittest
import pandas as pd
import sys


# this is ugly and not very robust
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "check"))

from checkSignalMonotonous import checkSignalMonotonous


class TestCheckSignalMonotonous(unittest.TestCase):

    def test_monotonous(self):

        signal = pd.Series([-3, 1, 4, 7])

        self.assertEqual(checkSignalMonotonous(signal), True)

    def test_notMonotonous(self):

        signal = pd.Series([1, 2, 3, 4, 1])

        self.assertEqual(checkSignalMonotonous(signal), False)


if __name__ == "__main__":
    unittest.main()
