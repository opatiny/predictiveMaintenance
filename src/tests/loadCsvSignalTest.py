import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)
from parse.loadCsvSignal import loadCsvSignal

# get the current folder path
currentPath = Path(__file__).resolve().parent
print(currentPath)

relFolderPath = "../../data/Mecatis/03_02_25/"
fileName = "lrSigSpindleTemp.csv"

filePath = str(currentPath / relFolderPath / fileName)

data = loadCsvSignal(filePath, debug=True)

print("data: ", data)

frequency = 1 / data["timeSeconds"].diff().mean()
print("frequency: ", frequency)
