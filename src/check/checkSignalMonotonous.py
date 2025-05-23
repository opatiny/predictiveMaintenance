import pandas as pd


def checkSignalMonotonous(time: pd.Series, debug: bool = False) -> bool:
    """
    Check if the signal is monotonous (must always increase).

    Parameters
    ----------
    time (pd.Series): The time series data.

    Returns
    -------
    bool: True if the time series is monotonous, False otherwise.
    """

    # compute the difference between consecutive time points
    diff = time.diff().dropna()

    if diff.min() <= 0:
        if debug:
            print("checkSignalMonotonous: Signal is not monotonous")
        return False
    else:
        if debug:
            print("checkSignalMonotonous: Signal is monotonous")
        return True
