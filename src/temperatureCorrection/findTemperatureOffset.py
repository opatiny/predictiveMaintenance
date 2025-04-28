import numpy as np
import pandas as pd
from scipy.optimize import minimize


def errorFun(x: float, data: pd.Series, reference: pd.Series) -> float:
    error = ((data - x - reference) ** 2).sum() / len(data)  # mean square error (MSE)
    return error


def findTemperatureOffset(temperature: pd.Series, reference: pd.Series) -> float:
    """
    Find the temperature offset that minimizes the error between the temperature and reference.

    Parameters
    ----------
    temperature (pd.Series): The temperature data.
    reference (pd.Series): The reference data.

    Returns
    -------
    float: The temperature offset.
    """
    x0 = 0.0  # start with an offset of 0°C
    result = minimize(errorFun, x0, args=(temperature, reference))
    return result.x[0], np.sqrt(result.fun)  # return the offset and the rmse
