import polars as pl
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/MILL/"
samplePath1 = "13-03-2025_7h35.parquet"

# load all data
data = pl.read_parquet(str(currentPath / machinePath / samplePath1))
print("data: ", data.shape)
print(data.columns)
print(data.head())
print(data.describe())
