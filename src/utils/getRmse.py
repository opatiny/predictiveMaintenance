import numpy as np
import pandas as pd


def getRmse(model: pd.Series, data: pd.Series) -> float:
    """
    Get the root mean square error (RMSE) between the model and the data.
    Parameters
    ----------
    model (pd.Series): The model.
    data (pd.Series): The data.
    """
    rmse = np.sqrt(((model - data) ** 2).sum() / len(data))
    return rmse
