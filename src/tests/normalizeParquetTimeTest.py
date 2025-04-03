import os
import sys
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from utils import Utils


data = pd.Series(
    [
        "2025-02-03T08:40:13.00Z",
        "2025-02-03T08:40:14.200Z",
        "2025-02-03T08:40:15Z",
    ]
)


result = Utils.normalizeParquetTime(data)

print("result: ", result)
