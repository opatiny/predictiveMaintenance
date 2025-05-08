import pandas as pd

import os
import sys

# add current folder to path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from utils import Utils


def loadCsvSignal(
    filePath: str, normalize: bool = False,  debug: bool = False
) -> pd.DataFrame:

    # Load data from csv file
    data = pd.read_csv(filePath, sep=";", header=None, names=["timestamp", "value"])

    if debug:
        print("getFormattedSignalData - Number of points to sort: ", data.shape[0])

    # sort data by time
    data = data.sort_values(by="timestamp")

    # remove duplicates
    data = Utils.removeDuplicatesFromCsv(data, debug)

    # convert time to seconds from beginning of array
    data.loc[:, "timeSeconds"] = Utils.normalizeCsvTime(data.loc[:, "timestamp"])

    # normalize the signal between -1 and 1
    if normalize:
        data.loc[:, "value"] = Utils.normalizeSignal(data.loc[:, "value"])

    # Select only the desired columns
    formattedData = data[["timeSeconds", "value"]]

    return formattedData
