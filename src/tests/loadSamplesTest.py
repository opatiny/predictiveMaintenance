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
from parse.loadSamples import loadSamples

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/MILL/"

# load all data
data, names = loadSamples(
    str(currentPath / machinePath),
    debug=True,
)

print("data: ", data)
