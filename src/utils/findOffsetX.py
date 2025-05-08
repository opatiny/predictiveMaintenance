import numpy as np
import pandas as pd
from scipy.optimize import minimize

from utils.findCommonSection import findCommonSection


def errorFun(offset: int, signal: pd.Series, reference: pd.Series) -> float:
    # hack to do an "integer" optimization
    intOffset = int(offset)
    common = findCommonSection(signal, reference, intOffset)
    commonSignal = common.loc[:, "signal"]
    commonReference = common.loc[:, "reference"]
    error = ((commonSignal - commonReference) ** 2).sum() / len(
        commonSignal
    )  # mean square error (MSE)

    print("offset: ", offset, "error: ", error)
    return error


def findOffsetX(
    signal: pd.Series,
    reference: pd.Series,
    maxOffsetFraction: float = 0.5,
    debug: bool = False,
) -> int:
    """
    Find the x offset that minimizes the error between the signal and reference.

    Parameters
    ----------
    signal (pd.Series): The signal data.
    reference (pd.Series): The reference data.
    maxOffsetFraction (float): The maximum offset as a fraction of the length of the smallest of the two signals.

    Returns
    -------
    int: The optimal x offset as an index to align signal on the reference.
    """

    maxOffset = int(
        maxOffsetFraction * min(len(signal), len(reference))
    )  # maximum offset in number of samples
    if debug:
        print("maxOffset: ", maxOffset)

    x0 = 0  # start with an offset of 0
    result = minimize(
        errorFun, x0, args=(signal, reference), bounds=[(-maxOffset, maxOffset)]
    )
    return result.x[0], np.sqrt(result.fun)  # return the offset and the rmse
