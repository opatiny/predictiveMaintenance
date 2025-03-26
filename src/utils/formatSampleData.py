import matplotlib.pyplot as plt
import pandas as pd
import math
import os
from pandas.core.frame import DataFrame

from utils import Utils


def formatSampleData(folderPath: str, debug: bool = False) -> DataFrame:

    # Get all files in the folder
    files = os.listdir(folderPath)
    if debug:
        print("files: ", files)

    fileName = files[0].split(".")[0]

    # Load data from csv file
    formattedData = pd.read_csv(
        folderPath + files[0], sep=";", header=None, names=["timestamp", fileName]
    )

    nbPoints = formattedData.shape[0]
    if debug:
        print("nbPoints: ", nbPoints)

    for file in files[1:]:
        # Load data from csv file
        data = pd.read_csv(
            folderPath + file, sep=";", header=None, names=["timestamp", "value"]
        )

        if data.shape[0] != nbPoints:
            print(
                "Error: the number of points in the files is different (folder: ",
                folderPath,
                ", file: ",
                file,
                ")",
            )
            return

        fileName = files[0].split(".")[0]
        formattedData[fileName] = data["value"]

    return formattedData
