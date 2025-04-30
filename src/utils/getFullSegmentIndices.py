def getFullSegmentIndices(segmentIndices: list) -> list:
    """
    Redefine segment indices to consider all points.
    Parameters
    ----------
    segmentIndices : list
        List of tuples with start and end indices of constant segments. This ignores transition phases.

    Returns
    -------
    list
        List of tuples with start and end indices of correction segments, which include all points of the signal.
    """
    correctionIndices = []
    firstSegment = [0, segmentIndices[0][1]]
    correctionIndices.append(firstSegment)
    for i in range(1, len(segmentIndices)):
        start = segmentIndices[i - 1][1] + 1
        end = segmentIndices[i][1]
        correctionIndices.append([start, end])
    return correctionIndices
