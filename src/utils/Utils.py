from datetime import datetime
import pandas as pd
import os

from sklearn.preprocessing import normalize


# TIME UTILS
def normalizeCsvTime(time: pd.Series) -> pd.Series:
    """
    Normalize timestamp in Microsoft filetime to seconds from beginning of array.
    """

    return (time - time.iloc[0]) / 1e7


def normalizeParquetTime(time: pd.Series) -> pd.Series:
    """
    Normalize time in parquet file to seconds from beginning of array.
    """
    epochs = pd.Series()

    for i in range(len(time)):
        date = parseStringDate(time[i])
        epoch = date.timestamp()
        epochs[i] = epoch

    return epochs - epochs[0]


def parseStringDate(date: str) -> datetime:
    """
    Parse a string date in the format %Y-%m-%dT%H:%M:%S.%fZ or %Y-%m-%dT%H:%M:%SZ into a datetime object.
    """
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for format in formats:
        try:
            return datetime.strptime(date, format)
        except ValueError:
            pass
    raise ValueError("no valid date format found")


def getDate(timestamp: int) -> str:
    """
    Convert Microsoft filetime to a human readable date.
    """

    zeroEpochInFt = 116444736000000000  # 1st January 1970 in filetime
    timestamp = (timestamp - zeroEpochInFt) / 1e7

    return pd.to_datetime(timestamp, unit="s").strftime("%Y-%m-%d %H:%M:%S")


# PLOT UTILS
def getYLabel(fileName: str) -> str:
    """
    Get the label for the y-axis of a plot from a file name.
    """

    fileAbsPath = os.path.abspath(__file__)
    fileDir = os.path.dirname(fileAbsPath)
    infoPath = fileDir + "/../../data/signalsDescription.csv"

    signalsInformation = pd.read_csv(infoPath, sep=",")

    signalIndex = signalsInformation[signalsInformation["fileName"] == fileName].index[
        0
    ]

    signalDescription = signalsInformation.loc[signalIndex, "description"]
    signalUnit = signalsInformation.loc[signalIndex, "unit"]

    return signalDescription + " [" + signalUnit + "]"


# OTHER


def removeDuplicates(signal: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    """
    Remove duplicates from a signal with timestamp and value columns.
    """

    originalLength = len(signal)
    signal = signal.drop_duplicates(subset=["timestamp"], keep="first")
    newLength = len(signal)

    if debug:
        print(f"removeDuplicates - Number duplicates: {originalLength - newLength}")

    # reset index
    signal = signal.reset_index(drop=True)

    return signal


def normalizeSignal(signal: pd.Series) -> pd.Series:
    """
    Normalize a signal between -1 and 1.
    """
    # normalize the signal between -1 and 1
    signal = normalize(signal.values.reshape(-1, 1), axis=0, norm="max").reshape(-1)

    return pd.Series(signal)
