import pandas as pd


def computeSlotsAverage(signal: pd.DataFrame, dt: float = 10) -> pd.DataFrame:
    """
    Compute the average of the signal in each time slot.

    Parameters
    ----------
    signal (pd.DataFrame): The signal to process. It must have a "timeSeconds" column.
    dt (float, optional): The duration of each slot in seconds.

    Returns
    -------
    pd.DataFrame: A DataFrame with the average value of the signal in each slot.
    """
    signal = signal.copy()
    slots = signal.loc[:, "timeSeconds"] // dt
    signal["slots"] = slots
    signal = signal.groupby("slots").mean()
    signal = signal.reset_index()
    signal = signal.drop(columns=["slots"])
    return signal
