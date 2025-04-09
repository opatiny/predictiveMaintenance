import pandas as pd


def detectConstantSegments(
    x: pd.Series, y: pd.Series, variation_threshold=0, min_points=5
):
    """
    Detect constant segments in the signal 'stSigSpindleVelocity', excluding segments where value is zero.

    Parameters:
    x (pd.Series): Time series data.
    y (pd.Series): Signal data.
    variation_threshold (float): The maximum allowed variation to consider the signal as constant.
    min_points (int): The minimum number of consecutive points for a segment to be considered constant.

    Returns:
    list: List of tuples with start and end indices of constant segments.
    """

    # Check if the input series have same length
    if len(x) != len(y):
        raise ValueError("Input series must have the same length")

    length = len(x)
    start_index = 0
    constantSegments = []

    for i in range(1, length):
        value_diff = abs(y.iloc[i] - y.iloc[i - 1])

        if value_diff > variation_threshold:
            if (i - start_index) >= min_points and y.iloc[start_index] != 0:
                constantSegments.append(
                    (
                        start_index,
                        i - 1,
                    )
                )

            start_index = i  # Reset start_index for new segment

    # Check the last segment
    if (length - start_index) >= min_points and y.iloc[start_index] != 0:
        constantSegments.append((start_index, length - 1))

    return constantSegments
