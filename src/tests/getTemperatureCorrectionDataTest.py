import os
from pathlib import Path
import sys

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from temperatureCorrection.getTemperatureCorrectionData import (
    getTemperatureCorrectionData,
)

dataPath = "../../data/normalized-2025_04_08/"

sample = "Mecatis_05_02_25.parquet"

samplePath = fileDir / Path(dataPath) / sample

data = getTemperatureCorrectionData(samplePath)

print("data: ", data)
