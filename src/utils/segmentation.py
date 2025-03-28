import numpy as np
import pandas as pd

def detectConstantSegments(data, variation_threshold=0, min_points=5):
    """
    Detect constant segments in the signal 'stSigSpindleVelocity', excluding segments where value is zero.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing 'timeSeconds' and 'value' columns.
    variation_threshold (float): The maximum allowed variation to consider the signal as constant.
    min_points (int): The minimum number of consecutive points for a segment to be considered constant.
    
    Returns:
    list: List of tuples with start and end times of constant segments.
    """
    constantSegments = []
    start_index = 0

    for i in range(1, len(data)):
        value_diff = abs(data['value'].iloc[i] - data['value'].iloc[i - 1])

        if value_diff > variation_threshold:
            if (i - start_index) >= min_points and data['value'].iloc[start_index] != 0:
                constantSegments.append((data['timeSeconds'].iloc[start_index], data['timeSeconds'].iloc[i - 1]))
            start_index = i  # Reset start_index for new segment

    # Check the last segment
    if (len(data) - start_index) >= min_points and data['value'].iloc[start_index] != 0:
        constantSegments.append((data['timeSeconds'].iloc[start_index], data['timeSeconds'].iloc[-1]))

    return constantSegments

# Example usage
data = pd.DataFrame({"timeSeconds": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "value": [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]})

constantSegments = detectConstantSegments(data, variation_threshold=0.1, min_points=3)
print(constantSegments)
