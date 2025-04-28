import pandas as pd
from signalProcessing import computeSlotsAverage, removeSegmentsBeginning, splitSignal
from utils.polyFit import evalModels, getPolyFits, getRelativeErrors


def temperatureCorrection(
    data: pd.DataFrame, segmentIndices: list[tuple], order: int = 3, debug: bool = False
) -> pd.Series:
    """
    Apply temperature correction to the data.
    Parameters
    ----------
    data (pd.DataFrame): The data to correct. Should contain the columns "timeSeconds", "temperature" and "current".
    segmentIndices (list): The indices of the start and end of each segment.
    order (int): The order of the polynomial fit.
    debug (bool): If True, print debug information.

    Returns
    -------
    pd.Series: The corrected spindle current.
    """
    segments = splitSignal(data, segmentIndices)
    # remove beginning of the signals
    cutSegments = removeSegmentsBeginning(segments, debug=debug)
    averagedSegments = []
    for i in range(len(cutSegments)):
        averagedSegments.append(computeSlotsAverage(cutSegments[i]))

    # get the polynomial fits
    models = getPolyFits(averagedSegments, order=order)
    segmentsWithFit = evalModels(averagedSegments, models)
    errors = getRelativeErrors(segmentsWithFit)
    if debug:
        print("Relative error in percents for each segment: ")
        print(errors.round(0))

    # we want to apply the temperature correction to all points
    # redefine segment indices
    correctionIndices = []
    firstSegment = [0, segmentIndices[0][1]]
    correctionIndices.append(firstSegment)
    for i in range(1, len(segmentIndices)):
        start = segmentIndices[i - 1][1] + 1
        end = segmentIndices[i][1]
        correctionIndices.append([start, end])
    if debug:
        print("Correction indices: ", correctionIndices)

    correctionSegments = splitSignal(data, correctionIndices)
    regressions = evalModels(correctionSegments, models)

    # subtract the polynomial fit from the initial data
    correctedCurrents = []
    totalLength = 0
    for i in range(len(correctionSegments)):
        originalCurrent = correctionSegments[i]["current"]
        regression = regressions[i]["polyFit"]
        # find expected constant current: first point of the averaged segment's regression
        initialCurrent = segmentsWithFit[i].loc[0, "polyFit"]
        if debug:
            print("Initial current: ", initialCurrent)
        correctedCurrents.append(originalCurrent - (regression - initialCurrent))
        totalLength += len(correctedCurrents[i])

    # concatenate the corrected current
    correctedCurrent = pd.concat(correctedCurrents, ignore_index=True)
    print("Corrected current dimensions: ", correctedCurrent.shape)

    return correctedCurrent
