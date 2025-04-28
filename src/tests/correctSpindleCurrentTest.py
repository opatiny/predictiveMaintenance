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

    # Correct the spindle current
    correctedCurrent = correctSpindleCurrent(data, debug=True)

    # Plot the corrected spindle current
    plt.plot(
        data["timeSeconds"], data["stSigAxCurrentS"], "o-", markersize=3, label=sample
    )
    plt.plot(data["timeSeconds"], correctedCurrent, "o-", markersize=3, label=sample)

plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.legend(["1", "1 corrected", "2", "2 corrected", "3", "3 corrected"])
plt.title("Corrected spindle current for different samples")
plt.grid()

plt.show()
