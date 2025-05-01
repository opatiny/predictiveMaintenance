import numpy as np
import pandas as pd
from scipy.optimize import minimize


def errorFun(x: float, data: pd.Series, reference: pd.Series) -> float:
    error = ((data - x - reference) ** 2).sum() / len(data)  # mean square error (MSE)
    return error


def findOffsetY(signal: pd.Series, reference: pd.Series) -> float:
    """
    Find the y offset that minimizes the error between the signal and reference.

    Parameters
    ----------
    signal (pd.Series): The signal data.
    reference (pd.Series): The reference data.

    Returns
    -------
    float: The optimal y offset.
    """
    x0 = 0.0  # start with an offset of 0°C
    result = minimize(errorFun, x0, args=(signal, reference))
    return result.x[0], np.sqrt(result.fun)  # return the offset and the rmse
