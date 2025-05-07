import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)
print("parentDir: ", parentDir)

sys.path.append(parentDir)

# import functions
from parse.loadSamples import loadSamples
from parse.saveNormalizedSamples import saveNormalizedSamples

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/MILL/"

# load all data
data, names = loadSamples(
    str(currentPath / machinePath),
    debug=True,
)

print("names: ", names)

# save data to parquet files

saveFolder = "normalized"
savePath = currentPath / "../../data" / saveFolder

print("savePath: ", savePath)

saveNormalizedSamples(data, names, savePath)

# load the data back
fileName = names[0] + ".parquet"

loadedData = pd.read_parquet(savePath / fileName)
