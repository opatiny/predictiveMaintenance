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

from parse.loadParquetSample import loadParquetSample
from plot.plotFrequency import plotFrequency


# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

dataPath = os.path.join(currentPath, "../../data/")

machineName = "MILL"
sampleName = "13-03-2025_7h35.parquet"

# load data
print("loading data...")
data = loadParquetSample(os.path.join(dataPath, machineName, sampleName), debug=True)

print("data: ", data.shape)
# print first rows
print(data.head())

# plot frequency
print("plotting frequency...")
plotFrequency(data["timeSeconds"], machineName + sampleName)

# save data to parquet
print("saving test parquet...")

fileName = machineName + "_" + sampleName.split(".")[0] + ".parquet"
normalizedDataFolder = "normalized"
data.to_parquet(os.path.join(dataPath, normalizedDataFolder, fileName), index=False)

# plot data
print("plotting data...")
plt.figure()
plt.plot(data["timeSeconds"], data["stSigAxCurrentB"], label="stSigAxCurrentB")
plt.grid()
plt.show()
