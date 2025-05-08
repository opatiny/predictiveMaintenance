import numpy as np
import os
from pandas.core.frame import DataFrame

from parse.loadCsvSignal import loadCsvSignal
from parse.getCurrentSignals import getCurrentSignals
from parse.convertToAmperes import convertToAmperes


def loadCsvSample(
    folderPath: str, currentUnit: str = "A", debug: bool = False
) -> DataFrame:
    """
    Load a sample in csv format and return a pandas dataframe.
      - Removes duplicates and normalizes time.
      - Removes columns that are full of NaN.
      - Linearly interpolates missing points.
      - Converts current to Amperes if necessary.

    Parameters
    ----------
    folderPath (str): The path to the folder containing the csv files.
    currentUnit (str): The unit of the current signals. Default is "A". Other options are "mA".
    debug (bool): If True, print debug information. Default is False.
    """
    # Get all files in the folder
    files = os.listdir(folderPath)
    if debug:
        print("formatSampleData - number of files to process: ", len(files))

    dfs = []
    lengths = []

    # load all of the files
    if debug:
        print("formatSampleData - loading files")

    # if necessary, convert current to Amperes
    currentSignals = getCurrentSignals()

    counter = 0
    for file in files:
        counter += 1
        # Get signal data
        signalData = loadCsvSignal(
            folderPath + "/" + file, normalize=False, debug=debug
        )

        # convert current to Amperes if necessary
        signalName = file.split(".")[0]
        if signalName in currentSignals:
            signalData = convertToAmperes(signalData, currentUnit)

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
