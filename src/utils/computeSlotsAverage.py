import pandas as pd


def computeSlotsAverage(signal: pd.DataFrame, dt: float = 10) -> pd.DataFrame:
    """
    Compute the average of the signal in each slot.

    Parameters
    ----------
    signal (pd.DataFrame): The signal to process. It must have a "timeSeconds" column.
    dt (float, optional): The duration of each slot in seconds.

    Returns
    -------
    pd.DataFrame: A DataFrame with the average value of the signal in each slot.
    """
    signal["slot"] = signal["timeSeconds"] // dt
    return signal.groupby("slot").mean()
