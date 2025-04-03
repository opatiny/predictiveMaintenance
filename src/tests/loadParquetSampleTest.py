import polars as pl
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from utils.loadParquetSample import loadParquetSample

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/MILL/"
samplePath1 = "13-03-2025_7h35.parquet"

# load data
print("loading data...")
data = loadParquetSample(
    os.path.join(currentPath, machinePath, samplePath1), debug=True
)

print("data: ", data.shape)
# print first rows
print(data.head())

# save n first rows as csv
nbPoints = data.shape[0] // 1000

print("saving test csv...")
data.head(nbPoints).to_csv("./test.csv", sep=",", index=False)

# plot data
print("plotting data...")
plt.figure()
plt.plot(data["stSigAxCurrentB"].dropna(), label="stSigAxCurrentB")
plt.show()
