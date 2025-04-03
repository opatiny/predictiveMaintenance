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

# import functions
from src.utils.loadCsvSample import loadCsvSample

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/Mecatis/"
samplePath1 = "Warmup_Mecatis_03_02_25/"

# load all data
data = loadCsvSample(
    folderPath=str(currentPath / machinePath / samplePath1),
    debug=True,
)

print("data: ", data.shape)

# save data to csv file
data.to_csv(
    "results" + "/formattedData.csv",
    sep=";",
    index=False,
)
