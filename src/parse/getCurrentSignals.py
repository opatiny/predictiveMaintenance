import os

import pandas as pd


def getCurrentSignals() -> list[str]:
    """
    Get the names of the signals that contain a current (in A or mA).
    Signals are in the "signalsDescription" file.
    """
    # Read signals descriptions
    fileAbsPath = os.path.abspath(__file__)
    fileDir = os.path.dirname(fileAbsPath)
    infoPath = fileDir + "/../../data/signalsDescription.csv"
    signalsInformation = pd.read_csv(infoPath, sep=",")

    # filter signals with unit "A"
    signalsWithCurrent = signalsInformation[signalsInformation["unit"] == "A"]

    # get the names of the signals
    signalNames = signalsWithCurrent["name"].tolist()

    return signalNames
