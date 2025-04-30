import pandas as pd
import time as timeLib


def detectConstantSegments(
    data: pd.DataFrame, variation_threshold=0, min_points=5, debug=False
):
    """
    Detect constant segments in the signal 'stSigSpindleVelocity', excluding segments where value is zero.

    Parameters:
    data (pd.DataFrame): The input data containing 'timeSeconds' and 'stSigSpindleVelocity' series.
    variation_threshold (float): The maximum allowed variation to consider the signal as constant.
    min_points (int): The minimum number of consecutive points for a segment to be considered constant.

    Returns:
    list: List of tuples with start and end indices of constant segments.
    """

    startTime = timeLib.time()

    time = data["timeSeconds"]
    command = data["stSigSpindleVelocity"]

    length = len(time)
    start_index = 0
    constantSegments = []

    for i in range(1, length):
        value_diff = abs(command.iloc[i] - command.iloc[i - 1])

        if value_diff > variation_threshold:
            if (i - start_index) >= min_points and command.iloc[start_index] != 0:
                constantSegments.append(
                    (
                        start_index,
                        i - 1,
                    )
                )

            start_index = i  # Reset start_index for new segment

    # Check the last segment
    if (length - start_index) >= min_points and command.iloc[start_index] != 0:
        constantSegments.append((start_index, length - 1))

    endTime = timeLib.time()
    if debug:
        print("Time to find constant segments: ", endTime - startTime)

    return constantSegments
