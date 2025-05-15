import os
import sys
from pathlib import Path
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)
print("parentDir: ", parentDir)

sys.path.append(parentDir)

from check.checkOverride import checkOverride

currentPath = Path(__file__).resolve().parent
print(currentPath)

relFilePath: Path = "../../data/normalized-2025_04_08/Locle_2025_03_18.parquet"

sample = pd.read_parquet(currentPath / relFilePath)
overrideMod = checkOverride(
    sample=sample,
    sampleName="Locle_2025_03_18",
    debug=True,
)

print(overrideMod)
