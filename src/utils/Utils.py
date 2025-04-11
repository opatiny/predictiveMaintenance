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

    # Add .000000Z only if fractional seconds are missing
    time = time.str.replace(
        r"(\.\d+)?Z$", lambda m: m.group(0) if m.group(1) else ".000000Z", regex=True
    )

    dates = pd.to_datetime(time, format="%Y-%m-%dT%H:%M:%S.%fZ", errors="coerce")

    seconds = dates.astype("int64") / 1e9

    relativeTime = seconds - seconds.iloc[0]

    return relativeTime.round(6)


def parseStringDate(date: str) -> datetime:
    """
    Parse a string date in the format %Y-%m-%dT%H:%M:%S.%fZ or %Y-%m-%dT%H:%M:%SZ into a datetime object.
    Note: datetime.strptime is super slow
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

    signalRow = signalsInformation[signalsInformation["fileName"] == fileName]

    if len(signalRow) == 0:
        print("Signal not found in signalsDescription.csv")
        return "Value"

    signalIndex = signalRow.index[0]

    signalDescription = signalsInformation.loc[signalIndex, "description"]
    signalUnit = signalsInformation.loc[signalIndex, "unit"]

    return signalDescription + " [" + signalUnit + "]"


# OTHER
def removeDuplicatesFromCsv(signal: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
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


def removeDuplicatesFromParquet(
    signal: pd.DataFrame, keep: str = "first", debug: bool = False
) -> pd.DataFrame:
    """
    Remove duplicates from a sample that comes from a parquet file.
    """

    originalLength = len(signal)
    signal = signal.drop_duplicates(subset=["time"], keep=keep)
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
