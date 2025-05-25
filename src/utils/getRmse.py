import numpy as np
import pandas as pd


def getRmse(reference: pd.Series, data: pd.Series) -> float:
    """
    Get the root mean square error (RMSE) between the reference and the data.
    Parameters
    ----------
    model (pd.Series): The model.
    data (pd.Series): The data.
    """
    if len(reference) != len(data):
        raise ValueError("Reference and data must have the same length.")
    rmse = np.sqrt(((reference - data) ** 2).sum() / len(data))
    return rmse
