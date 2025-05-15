import pandas as pd


def checkMissingPoints(time: pd.Series) -> bool:
    """
    Check if there are any missing points in the time series.

    Parameters
    ----------
    time (pd.Series): The time series data.

    Returns
    -------
    bool: True if there are missing points, False otherwise.
    """

    # compute the difference between consecutive time points
    diff = time.diff().dropna()
    # verify that the difference is constant
    if diff.nunique() == 1:
        return False
    else:
        Warning("Signal is missing points")
        return True
