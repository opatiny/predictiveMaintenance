import numpy as np
import pandas as pd
from scipy.optimize import minimize


def evalPolyReg(p: list[float], data: pd.DataFrame) -> pd.Series:
    """
    Evaluate a polynomial regression model.
    Parameters
    ----------
    p (list): The parameters of the model.
    data (pd.DataFrame): The data, which should have 2 columns.
    """
    x = data.iloc[:, 0]  # the first column is the x value
    result = pd.Series([p[0]] * len(x))  # the first parameter is the offset
    for i in range(1, len(p)):
        result += p[i] * x**i
    return result


def errorFun(p: list, data: pd.DataFrame) -> float:
    """
    Function for a polynomial regression model.
    y = p[0] + p[1] * x + p[2] * x^2 + ... + p[n] * x^n
    Parameters
    ----------
    p (list): The parameters of the model.
    data (pd.DataFrame): The data, which should have 2 columns.
    """

    # check if the data has 2 columns
    if len(data.columns) != 2:
        raise ValueError("The data must have 2 columns.")

    model = evalPolyReg(p, data)
    y = data.iloc[:, 1]
    error = ((y - model) ** 2).sum() / len(data)  # mean square error (MSE)
    return error


# there's a bug with order 2 and more
def getPolyRegression(data: pd.DataFrame, order=1) -> list:
    x0 = [0.0] * (order + 1)
    result = minimize(errorFun, x0, args=(data))
    return result.x, np.sqrt(result.fun)  # return the weights and the rmse
