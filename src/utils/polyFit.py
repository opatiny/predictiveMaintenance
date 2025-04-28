import numpy as np
import pandas as pd

from utils.getRmse import getRmse


def getPolyFits(segments: list[pd.DataFrame], order: int = 1) -> list[np.poly1d]:
    """
    Get the polynomial fits for each segment.
    Parameters
    ----------
    segments (list[pd.DataFrame]): The segments of the signal.
    order (int): The order of the polynomial fit.
    """
    models = []
    for segment in segments:
        model = np.poly1d(np.polyfit(segment["temperature"], segment["current"], order))
        models.append(model)
    return models


def evalModels(
    segments: list[pd.DataFrame], models: list[np.poly1d]
) -> list[pd.DataFrame]:
    """
    Evaluate the polynomial fits for each segment.
    Parameters
    ----------
    segments (list[pd.DataFrame]): The segments of the signal.
    models (list[np.poly1d]): The polynomial fits for each segment.
    """
    for i in range(len(segments)):
        segments[i] = segments[i].copy()  # Ensure it's a copy
        segments[i].loc[:, "polyFit"] = models[i](segments[i].loc[:, "temperature"])
    return segments


def getErrors(segments: list[pd.DataFrame]) -> list[float]:
    """
    Compute rmse between measurement and polynomial regression for each segment.
    """
    errors = []
    for segment in segments:
        error = getRmse(segment["polyFit"], segment["current"])
        errors.append(error)
    return errors


def getRelativeErrors(segments: list[pd.DataFrame]) -> pd.Series:
    """
    Compute the relative errors in **percents** for each segment. The absolute RMSE is divided by the range of the signal.
    """
    relativeErrors = []
    for segment in segments:
        maxValue = segment["current"].max()
        min = segment["current"].min()
        diff = maxValue - min
        error = getRmse(segment["polyFit"], segment["current"])
        relativeErrors.append(error / diff * 100)  # in percent

    return pd.Series(relativeErrors)
