import pandas as pd

import os
import sys
import time

# add current folder to path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import Utils


def getFormattedSignalData(filePath: str, debug: bool = False) -> pd.DataFrame:
    # Load data from csv file
    data = pd.read_csv(filePath, sep=";", header=None, names=["timestamp", "value"])

    if debug:
        print("Number of points to sort: ", data.shape[0])

    # sort data by time
    start_time = time.time()
    data = data.sort_values(by="timestamp")
    end_time = time.time()

    if debug:
        print(f"Time to sort: {end_time - start_time:.6f} seconds")

    # convert time to seconds from beginning of array
    start_time = time.time()
    data.loc[:, "timeSeconds"] = Utils.getNormalizedTime(data.loc[:, "timestamp"])
    end_time = time.time()

    if debug:
        print(f"Time to normalize: {end_time - start_time:.6f} seconds")

    # Select only the desired columns
    formattedData = data[["timeSeconds", "value"]]

    return formattedData
