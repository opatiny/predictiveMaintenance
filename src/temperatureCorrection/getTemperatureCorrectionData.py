from pathlib import Path
import pandas as pd

from utils.computeSlotsAverage import computeSlotsAverage


def getTemperatureCorrectionData(
    data: pd.DataFrame, timeSlot: float = 10, debug: bool = False
) -> pd.DataFrame:
    """
    Get the current and temperature data from a sample path.

    Parameters
    ----------
    sample (pd.DataFrame): The data to process.
    timeSlot (float): The duration of each slot on which to average in seconds.
        Defaults to 10 seconds.
    debug (bool, optional): Whether to print debug information. Defaults to True.

    Returns
    -------
    pd.DataFrame: The time, spindle current and spindle temperature data.
    """
    temperatureSlots = data[["timeSeconds", "lrSigSpindleTemp"]]
    currentSlots = data[["timeSeconds", "stSigAxCurrentS"]]
    if timeSlot != None:
        temperatureSlots = computeSlotsAverage(temperatureSlots, timeSlot)
        currentSlots = computeSlotsAverage(currentSlots, timeSlot)

    # merge the data
    result = pd.DataFrame()
    result["timeSeconds"] = temperatureSlots["timeSeconds"]
    result["temperature"] = temperatureSlots.iloc[:, 1]
    result["current"] = currentSlots.iloc[:, 1]

    return result
