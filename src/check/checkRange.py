import os
import pandas as pd


def checkRange(signal: pd.Series, name: str, debug: bool = False) -> bool:
    """
    Check if a signal is in the desired range or not.

    Args:
        sample (pd.Series): The signal to check.
        name (str): The name of the signal.
        debug (bool): If True, print debug information.

    Returns:
        bool: True if the signal is in range, False otherwise.
    """
    # find min and max values

    fileAbsPath = os.path.abspath(__file__)
    fileDir = os.path.dirname(fileAbsPath)
    infoPath = fileDir + "/../../data/signalsDescription.csv"

    signalsInformation = pd.read_csv(infoPath, sep=",")
    signalRow = signalsInformation[signalsInformation["name"] == name]
    if len(signalRow) == 0:
        NameError("checkRange: Signal name not found in signalsDescription.csv")

    minValue = signalRow["min"].values[0]
    maxValue = signalRow["max"].values[0]

    if debug:
        print(f"Signal {name} min: {minValue}, max: {maxValue}")

    # check if the signal is in the desired range
    if signal.min() < minValue or signal.max() > maxValue:
        if debug:
            print(f"Signal {name} is out of range")
        return False
    else:
        if debug:
            print(f"Signal {name} is in range")
        return True
