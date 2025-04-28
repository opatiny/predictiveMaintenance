import pandas as pd
from signalProcessing.splitSignal import splitSignal
from signalProcessing.removeSegmentsBeginning import removeSegmentsBeginning
from signalProcessing.computeSlotsAverage import computeSlotsAverage
from temperatureCorrection.getTemperatureCorrectionData import (
    getTemperatureCorrectionData,
)
from utils.detectConstantSegments import detectConstantSegments
from utils.polyFit import evalModels, getPolyFits, getRelativeErrors
import time as timeLib


def correctSpindleCurrent(
    rawData: pd.DataFrame,
    order: int = 3,
    debug: bool = False,
) -> pd.Series:
    """
    Apply temperature correction to spindle current.
    Parameters
    ----------
    data (pd.DataFrame): The sample data. The function will correct the spindle current.
    order (int): The order of the polynomial fit.
    debug (bool): If True, print debug information.

    Returns
    -------
    pd.Series: The corrected spindle current.
    """

    # format data
    time = rawData["timeSeconds"]
    command = rawData["stSigSpindleVelocity"]
    startTime = timeLib.time()
    segmentIndices = detectConstantSegments(time, command)
    endTime = timeLib.time()
    print("Time to find constant segments: ", endTime - startTime)
    data = getTemperatureCorrectionData(rawData, timeSlot=None)

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
        # if debug:
        #     print("Initial current: ", initialCurrent)
        correctedCurrents.append(originalCurrent - (regression - initialCurrent))
        totalLength += len(correctedCurrents[i])

    # concatenate the corrected current
    correctedCurrent = pd.concat(correctedCurrents, ignore_index=True)

    return correctedCurrent
