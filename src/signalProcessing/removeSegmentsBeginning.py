import pandas as pd


def removeSegmentsBeginning(
    segments: list[pd.DataFrame], timeToRemove: float = 0.5, debug: bool = False
) -> list[pd.DataFrame]:
    """
    Remove the first timeToRemove seconds from each segment. Allows to only consider the steady state of the signal.
    """

    # compute the frequency of the signal
    averageDiff = 0
    for i in range(len(segments) - 1):
        averageDiff += segments[i + 1].iloc[0, 0] - segments[i].iloc[0, 0]
    averageDiff /= len(segments) - 1
    frequency = 1 / averageDiff  # in Hz

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
