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
      - Interpolates the whole signal at a given frequency.
      - Converts current to Amperes if necessary.

    Parameters
    ----------
    folderPath (str): The path to the folder containing the csv files.
    currentUnit (str): The unit of the current signals. Default is "A". Other options are "mA".
    debug (bool): If True, print debug information. Default is False.
    """

    # frequency of the signal
    frequency = 2000  # Hz

    # Get all files in the folder
    files = os.listdir(folderPath)
    if debug:
        print("formatSampleData - number of files to process: ", len(files))

    signals = []
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

        signals.append(signalData)
        lengths.append(signalData.shape[0])

        if debug:
            print("file: ", file, "(", counter, "/", len(files), ")")

    # find signal with the most points
    maxLength = max(lengths)
    if debug:
        print("formatSampleData - initial nb of points: ", maxLength)
    index = lengths.index(maxLength)
    fileName = files[index].split(".")[0]

    # create new time vector
    minTime = signals[index]["timeSeconds"].min()
    maxTime = signals[index]["timeSeconds"].max()
    timeVector = np.arange(minTime, maxTime, 1 / frequency)

    # create a new dataframe
    formattedSampleData = DataFrame()
    formattedSampleData["timeSeconds"] = timeVector

    if debug:
        print("formatSampleData - interpolating signals")

    # interpolate all signals
    for i in range(len(signals)):
        fileName = files[i].split(".")[0]

        # Interpolate the signal if less than the max length
        interpolated = np.interp(
            formattedSampleData["timeSeconds"],
            signals[i]["timeSeconds"],
            signals[i]["value"],
        )
        formattedSampleData[fileName] = interpolated

    if debug:
        print("formatSampleData - final nb of points: ", formattedSampleData.shape[0])

    return formattedSampleData
