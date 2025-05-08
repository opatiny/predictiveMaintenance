import os
import sys
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from utils.findOffsetX import findOffsetX

signal = pd.Series([1, 2, 3, 4, 5, 0, 0, 0, 0, 0])
reference = pd.Series([0, 0, 0, 0, 0, 1, 2, 3, 4, 5])

offset = findOffsetX(signal, reference)

print("Offset: ", offset)
