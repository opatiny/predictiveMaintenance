import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
from pandas.core.frame import DataFrame

from loadCsvSignal import loadCsvSignal


def loadCsvSample(folderPath: str, debug: bool = False) -> DataFrame:

    # Get all files in the folder
    files = os.listdir(folderPath)
    if debug:
        print("formatSampleData - number of files to process: ", len(files))

    dfs = []
    lengths = []

    # load all of the files
    if debug:
        print("formatSampleData - loading files")

    counter = 0
    for file in files:
        counter += 1
        # Get signal data
        signalData = loadCsvSignal(
            folderPath + "/" + file, normalize=False, debug=debug
        )

        dfs.append(signalData)
        lengths.append(signalData.shape[0])

        if debug:
            print("file: ", file, "(", counter, "/", len(files), ")")

    # find signal with the most points
    maxLength = max(lengths)
    if debug:
        print("formatSampleData - max nb of points: ", maxLength)
    index = lengths.index(maxLength)
    fileName = files[index].split(".")[0]

    formattedSampleData = dfs[index]
    formattedSampleData.rename(columns={"value": fileName}, inplace=True)

    print(formattedSampleData.columns)

    nbInterpolations = 0

    if debug:
        print("formatSampleData - interpolating signals")

    # add other signals and interpolate if necessary
    for i in range(len(dfs)):
        fileName = files[i].split(".")[0]
        if i != index:
            if len(dfs[i]) < maxLength:
                nbInterpolations += 1

                # Interpolate the signal if less than the max length
                interpolated = np.interp(
                    formattedSampleData["timeSeconds"],
                    dfs[i]["timeSeconds"],
                    dfs[i]["value"],
                )
                formattedSampleData[fileName] = interpolated
            else:
                # Add the signal to the formatted data
                formattedSampleData[fileName] = dfs[i]["value"]

    if debug:
        print("formatSampleData - Number of signals interpolatedd: ", nbInterpolations)

    return formattedSampleData
