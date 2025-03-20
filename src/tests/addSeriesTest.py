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
from addSeries import addSeries

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

machinePath = "../../data/Machine#1_Mecatis/"
samplePath1 = "Warmup_Mecatis_03_02_25/"
samplePath2 = "Warmup_Mecatis_05_02_25/"
samplePath3 = "Warmup_Mecatis_17_02_25/"
file = "stSigAxCurrentS.csv"


# concanetating the path
path1 = str(currentPath / machinePath / samplePath1 / file)
path2 = str(currentPath / machinePath / samplePath2 / file)
path3 = str(currentPath / machinePath / samplePath3 / file)

nbPoints = None


plt.figure()
plt.title("Spindle currents from various samples (Mecatis)")
plt.xlabel("Time [s]")
plt.ylabel("Current [mA]")
plt.grid(True)

addSeries(path1, nbPoints)
addSeries(path2, nbPoints)
addSeries(path3, nbPoints)

plt.legend([samplePath1, samplePath2, samplePath3])
plt.show()

# Close all plots
plt.close("all")
