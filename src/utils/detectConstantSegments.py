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
    list: List of tuples with start and end times of constant segments.
    """
    length = len(x)
    start_index = 0
    constantSegments = []

    for i in range(1, length):
        value_diff = abs(y.iloc[i] - y.iloc[i - 1])

        if value_diff > variation_threshold:
            if (i - start_index) >= min_points and y.iloc[start_index] != 0:
                constantSegments.append(
                    (
                        x.iloc[start_index],
                        x.iloc[i - 1],
                    )
                )

            start_index = i  # Reset start_index for new segment

    # Check the last segment
    if (length - start_index) >= min_points and y.iloc[start_index] != 0:
        constantSegments.append((x.iloc[start_index], x.iloc[-1]))

    return constantSegments


# Example usage

x = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = pd.Series([1, 1, 1, 2, 2, 2, 3, 3, 3, 3])

constantSegments = detectConstantSegments(x, y, variation_threshold=0.1, min_points=3)
print(constantSegments)
