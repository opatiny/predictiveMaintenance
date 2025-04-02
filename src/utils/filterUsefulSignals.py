import os

import pandas as pd


def filterUsefulSignals(data: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    """
    Filter the useful signals from the dataframe as defined in the signalsDescription.csv file.
    The signalsDescription.csv file is located in the data folder.
    """
    fileAbsPath = os.path.abspath(__file__)
    fileDir = os.path.dirname(fileAbsPath)
    infoPath = fileDir + "/../../data/signalsDescription.csv"
    signalsInformation = pd.read_csv(infoPath, sep=",")

    # only keep the interesting signals from the folder

    usefulSignals = signalsInformation[signalsInformation["useful"] == 1]

    # Filter the dataframe
    filteredData = data[usefulSignals]

    if debug:
        print("filterUsefulSignals - filtered data: ", filteredData.shape)
        print(filteredData.head())

    return filteredData
