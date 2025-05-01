import os
from pathlib import Path
import sys

from matplotlib import pyplot as plt
import pandas as pd

# append parent directory to path
fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

sys.path.append(parentDir)

from utils.detectConstantSegments import detectConstantSegments
from temperatureCorrection.correctSpindleCurrent import correctSpindleCurrent


dataPath: Path = "../../data/normalized-2025_04_08/"

samples = [
    "Mecatis_05_02_25.parquet",
    "Mecatis_17_02_25.parquet",
    # "Mecatis_10_03_25.parquet",
]


plt.figure()
for sample in samples:
    print("Current sample: ", sample)

    # Load the data
    samplePath = fileDir / Path(dataPath) / sample
    data = pd.read_parquet(samplePath)

    segmentIndices = detectConstantSegments(data)

    # Correct the spindle current
    correctedCurrent = correctSpindleCurrent(data, segmentIndices, debug=True)

    # Plot the corrected spindle current
    plt.plot(
        data["lrSigSpindleTemp"],
        data["stSigAxCurrentS"],
        "o-",
        markersize=3,
        label=sample,
    )
    plt.plot(
        data["lrSigSpindleTemp"], correctedCurrent, "o-", markersize=3, label=sample
    )

plt.xlabel("Temperature (°C)")
plt.ylabel("Current (A)")
plt.legend(["1", "1 corrected", "2", "2 corrected", "3", "3 corrected"])
plt.title("Corrected spindle current versus temperature for different samples")
plt.grid()

plt.show()
