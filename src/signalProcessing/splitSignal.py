import pandas as pd


def splitSignal(data: pd.DataFrame, indices: list) -> list[pd.DataFrame]:
    """
    Split the data into segments using the given start and end indices of each segment.

    Parameters
    ----------
    signal (pd.DataFrame): The data, which can have any number of columns.
    indices (list): The start and end indices of the segments.

    Returns
    -------
    list[pd.DataFrame]: The segments of the signal.
    """
    segments = []
    for segment in indices:
        segments.append(data.iloc[segment[0] : segment[1] + 1])
    return segments


def splitSignalByOperation(
    data: pd.DataFrame, indices: list[int]
) -> list[pd.DataFrame]:
    """
    Split the data into segments using a list of indices where to cut the dataframe.

    Parameters
    ----------
    signal (pd.DataFrame): The data, which can have any number of columns.
    indices (list[int]): The the start indices of the segments.

    Returns
    -------
    list: The segments of the signal.
    """
    segments = []
    for i in range(len(indices) - 1):
        start = indices[i]
        end = indices[i + 1] - 1

        print("start: ", start)
        print("end: ", end)
        segment = data.iloc[start:end, :]
        segments.append(segment)
    # add the last segment
    start = indices[-1]
    end = len(data)
    segment = data.iloc[start:end, :]
    segments.append(segment)
    return segments
