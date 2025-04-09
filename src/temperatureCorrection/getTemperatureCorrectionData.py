from pathlib import Path
import pandas as pd

from utils.computeSlotsAverage import computeSlotsAverage


def getTemperatureCorrectionData(
    samplePath: Path, timeSlot: float = 10, debug: bool = False
) -> pd.DataFrame:
    """
    Get the current and temperature data from a sample path.

    Parameters
    ----------
    samplePath (str): The path to the sample.
    timeSlot (float): The duration of each slot on which to average in seconds.
        Defaults to 10 seconds.
    debug (bool, optional): Whether to print debug information. Defaults to True.

    Returns
    -------
    pd.DataFrame: The time, spindle current and spindle temperature data.
    """
    # load the data
    data = pd.read_parquet(samplePath)
    temperatureSlots = data[["timeSeconds", "lrSigSpindleTemp"]]
    currentSlots = data[["timeSeconds", "stSigAxCurrentS"]]
    if timeSlot != None:
        temperatureSlots = computeSlotsAverage(temperatureSlots, timeSlot)
        currentSlots = computeSlotsAverage(currentSlots, timeSlot)

    # merge the data
    data = pd.DataFrame()
    data["timeSeconds"] = temperatureSlots["timeSeconds"]
    data["temperature"] = temperatureSlots["value"]
    data["current"] = currentSlots["value"]

    return data
