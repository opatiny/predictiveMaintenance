import pandas as pd


def getNormalizedTime(time: pd.Series) -> pd.Series:
    """
    Normalize timestamp in Microsoft filetime to seconds from beginning of array.
    """

    return (time - time.iloc[0]) / 1e7


def getDate(timestamp: int) -> str:
    """
    Convert Microsoft filetime to a human readable date.
    """

    zeroEpochInFt = 116444736000000000  # 1st January 1970 in filetime
    timestamp = (timestamp - zeroEpochInFt) / 1e7

    return pd.to_datetime(timestamp, unit="s").strftime("%Y-%m-%d %H:%M:%S")


def getYLabel(fileName: str) -> str:
    """
    Get the label for the y-axis of a plot from a file name.
    """

    signalsInformation = pd.read_csv("data/signalsDescription.csv", sep=",")
    signalIndex = signalsInformation[signalsInformation["fileName"] == fileName].index[
        0
    ]

    signalDescription = signalsInformation.loc[signalIndex, "description"]
    signalUnit = signalsInformation.loc[signalIndex, "unit"]

    return signalDescription + " [" + signalUnit + "]"
