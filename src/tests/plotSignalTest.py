import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt

fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from plotSignal import plotSignal

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

relFolderPath = "../../data/Machine#1_Mecatis/Warmup_Mecatis_03_02_25/"
fileName = "stSigAxCurrentB.csv"

# concanetating the path
filePath = str(currentPath / relFolderPath / fileName)
print("filePath: ", filePath)
plotSignal(filePath)
plt.show()

# Close all plots
plt.close("all")
