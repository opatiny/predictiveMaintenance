# append parent directory to path
import os
from pathlib import Path
import sys

from matplotlib import pyplot as plt
import pandas as pd


fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

dataPath: Path = "../../data/normalized-2025_04_08/"

sampleNames = [
    "Mecatis_05_02_25.parquet",
    "Mecatis_17_02_25.parquet",
    "Locle_2025_03_18.parquet",
    "MILL_13-03-2025_7h35.parquet",
]

inMillisAmperes = [1, 1, 0, 0]

correctedDatas: list[pd.DataFrame] = []

datas = []

for sample in sampleNames:
    # Load the data
    samplePath = fileDir / Path(dataPath) / sample
    data = pd.read_parquet(samplePath)
    datas.append(data)


# plot spindle current from each sample
plt.figure()
for i, data in enumerate(datas):
    if inMillisAmperes[i]:
        data["stSigSpindleIndicator"] = data["stSigSpindleIndicator"] / 1000

    plt.plot(
        data["timeSeconds"],
        data["stSigSpindleIndicator"],
        # data["stSigAxCurrentS"],
        # "o-",
        # markersize=3,
        label=sampleNames[i].split(".")[0],
    )
plt.title("Spindle current")
plt.xlabel("Time [s]")
plt.ylabel("Current [A]")
plt.grid()
plt.legend()
plt.show()
