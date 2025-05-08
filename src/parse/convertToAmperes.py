import pandas as pd


def convertToAmperes(signal: pd.Series, unit: str) -> pd.Series:
    """
    Convert the signal to Amperes if the unit is in mA.

    Parameters
    ----------
    signal (pd.Series): The signal data.
    unit (str): The unit of the signal. Can be 'A' or 'mA'.

    Returns
    -------
    pd.Series: The converted signal in Amperes.
    """
    if unit == "mA":
        return signal / 1000
    elif unit == "A":
        return signal
    else:
        raise ValueError("Unknown current unit: " + unit + ". Use 'A' or 'mA'.")
