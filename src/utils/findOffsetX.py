import numpy as np
import pandas as pd
from scipy.signal import correlate


def findOffsetX(
    signal: pd.Series,
    reference: pd.Series,
) -> int:
    """
    Find the x offset that minimizes the error between the signal and reference.
    Uses the correlation between the two signals.

    Parameters
    ----------
    signal (pd.Series): The signal data.
    reference (pd.Series): The reference data.

    Returns
    -------
    int: The optimal x offset as an index to align signal on the reference.
    """

    correlation = correlate(signal, reference, mode="full")
    # Find the index of the maximum correlation
    max_index = np.argmax(correlation)
    # Calculate the offset
    offset = (len(reference) - 1) - max_index

    return offset
