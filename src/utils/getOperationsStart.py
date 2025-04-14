import pandas as pd


def getOperationsStart(data: pd.Series) -> list:
    """
    Detect constant segments in the data using the "stSigOperation" signal.

    Parameters:

    Returns:
    list[int]: List of the start index of each segment
    """
    # find the indices where the signal is constant
    indices = [0]
    start_index = 0
    for i in range(1, len(data)):
        if data[i] != data[i - 1]:
            indices.append(i)
    return indices
