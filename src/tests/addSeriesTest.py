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

file1 = "stSigAxCurrentS.csv"
file2 = "lrSigSpindleTemp.csv"


# concanetating the path

samplePath = samplePath1
path1 = str(currentPath / machinePath / samplePath / file1)
path2 = str(currentPath / machinePath / samplePath / file2)

nbPoints = None


plt.figure()
plt.title(samplePath + ": Spindle current and target speed")
plt.xlabel("Time [s]")
plt.ylabel("Normalized signals")
plt.grid(True)

baseOptions = {"nbPoints": nbPoints, "normalize": True, "debug": True}

# addSeries(path1, baseOptions)
addSeries(path2, baseOptions)

plt.legend(
    ["Normalized current", "Normalized target speed"],
    loc="upper right",
)
plt.show()

# Close all plots
plt.close("all")
