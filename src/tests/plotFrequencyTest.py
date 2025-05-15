import os
import sys
from pathlib import Path
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)
print("parentDir: ", parentDir)

sys.path.append(parentDir)

from plot.plotFrequency import plotFrequency
from parse.loadCsvSignal import loadCsvSignal

currentPath = Path(__file__).resolve().parent
print(currentPath)

folderPath: Path = "../../data/normalized-2025_05_08"

fileNames = [
    "Locle_2025_03_18.parquet",
    "Mecatis_03_02_25.parquet",
    "MILL_13-03-2025_7h35.parquet",
]

fileName = fileNames[2]

relFilePath = os.path.join(folderPath, fileName)

sample = pd.read_parquet(currentPath / relFilePath)

plotFrequency(sample["timeSeconds"], fileName)


# compare with data before normlization

samplePath: Path = "../../data/Mecatis/03_02_25"

fileName = "stSigAxCurrentS.csv"

relFilePath = os.path.join(samplePath, fileName)

signal = loadCsvSignal(currentPath / relFilePath)

plotFrequency(signal["timeSeconds"], fileName)
