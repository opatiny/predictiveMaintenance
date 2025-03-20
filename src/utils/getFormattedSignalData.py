import pandas as pd

# add current folder to path
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import Utils


def getFormattedSignalData(filePath: str) -> pd.DataFrame:
    # Load data from csv file
    data = pd.read_csv(filePath, sep=";", header=None, names=["timestamp", "value"])

    # sort data by time
    data = data.sort_values(by="timestamp")

    # convert time to seconds from beginning of array
    data.loc[:, "timeSeconds"] = Utils.getNormalizedTime(data.loc[:, "timestamp"])

    # Select only the desired columns
    formattedData = data[["timeSeconds", "value"]]

    return formattedData
