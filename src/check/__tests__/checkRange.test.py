from pathlib import Path
import unittest
import pandas as pd
import sys


# this is ugly and not very robust
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "check"))

from checkRange import checkRange


class TestCheckRange(unittest.TestCase):

    def test_inRange(self):

        signal = pd.Series([1, 2, 3, 4, 5])
        name = "lrSigSpindleTemp"

        self.assertEqual(checkRange(signal, name), True)

    def test_outOfRange(self):

        signal = pd.Series([0, 0, 200])
        name = "lrSigSpindleTemp"

        self.assertEqual(checkRange(signal, name), False)


if __name__ == "__main__":
    unittest.main()
