import pandas as pd

# add current folder to path
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import Utils


def getFormattedSignalData(filePath: str, debug: bool = False) -> pd.DataFrame:
    # Load data from csv file
    data = pd.read_csv(filePath, sep=";", header=None, names=["timestamp", "value"])

    if debug:
        print("Number of points to sort: ", data.shape[0])

    # sort data by time
    data = data.sort_values(by="timestamp")

    # convert time to seconds from beginning of array
    data.loc[:, "timeSeconds"] = Utils.getNormalizedTime(data.loc[:, "timestamp"])

    # Select only the desired columns
    formattedData = data[["timeSeconds", "value"]]

    return formattedData
