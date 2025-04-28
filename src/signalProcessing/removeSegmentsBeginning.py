import pandas as pd

from utils.Utils import getFrequency


def removeSegmentsBeginning(
    segments: list[pd.DataFrame], timeToRemove: float = 0.5, debug: bool = False
) -> list[pd.DataFrame]:
    """
    Remove the first timeToRemove seconds from each segment. Allows to only consider the steady state of the signal.
    """

    frequency = getFrequency(segments[0])  # frequency in Hz

    if debug:
        print("Frequency: ", frequency, "Hz")

    nbPointsToRemove = int(timeToRemove * frequency)  # number of points to remove
    if debug:
        print("Number of points to remove: ", nbPointsToRemove)

    cutSegments = []

    for i in range(len(segments)):
        # remove the first nbPointsToRemove points
        cutSegments.append(segments[i].iloc[nbPointsToRemove:, :])
    return cutSegments
