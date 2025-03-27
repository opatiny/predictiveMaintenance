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
from utils.addSeries import addSeries

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/Mecatis/"
samplePath1 = "Warmup_Mecatis_03_02_25"
samplePath2 = "Warmup_Mecatis_05_02_25"
samplePath3 = "Warmup_Mecatis_17_02_25"

file1 = "stSigAxCurrentB.csv"
file2 = "stSigAxPosACSB.csv"
file3 = "stSigAxVeloACSB.csv"


# concanetating the path
path1 = str(currentPath / machinePath / samplePath1 / file1)
path2 = str(currentPath / machinePath / samplePath1 / file2)
path3 = str(currentPath / machinePath / samplePath1 / file3)

nbPoints = 300000


plt.figure()
plt.title(samplePath1 + ": Current, position and velocity of axis B")
plt.xlabel("Time [s]")
plt.ylabel("Normalized signals")
plt.grid(True)

baseOptions = {"nbPoints": nbPoints, "normalize": True}

addSeries(path1, baseOptions)
addSeries(path2, baseOptions)
addSeries(path3, baseOptions)

plt.legend(
    ["Normalized current", "Normalized ACS position", "Normalized ACS velocity"],
    loc="upper right",
)
plt.show()

# Close all plots
plt.close("all")
