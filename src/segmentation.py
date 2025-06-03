# src/segmentation.py

import pandas as pd
from typing import List, Tuple

def detect_stable_segments(
    data: pd.DataFrame,
    signal_column: str,
    window: int,
    std_threshold: float,
    min_length: int,
    max_segments: int,
    min_stable_duration: int,
    min_segment_duration: float
) -> List[Tuple[float, float]]:
    """
    Detect stable segments in a signal based on rolling standard deviation.

    Args:
        data (pd.DataFrame): DataFrame containing time and signal data.
        signal_column (str): Name of the column with the signal to analyze.
        window (int): Window size for rolling standard deviation.
        std_threshold (float): Maximum std deviation to consider segment stable.
        min_length (int): Minimum length (in number of points) for a stable segment.
        max_segments (int): Maximum number of segments to detect.
        min_stable_duration (int): Minimum consecutive points below std threshold to start a stable segment.
        min_segment_duration (float): Minimum segment duration (in time units) for valid segment.

    Returns:
        List[Tuple[float, float]]: List of detected stable segments as (start_time, end_time).
    """
    # Determine time column (prefer gapless time if available)
    time_col = 'timeSeconds_nogap' if 'timeSeconds_nogap' in data.columns else 'timeSeconds'

    signal = data[signal_column]
    rolling_std = signal.rolling(window=window, center=True).std()
    stable_mask = rolling_std < std_threshold

    segments = []
    start_idx = None
    stable_count = 0

    for i, is_stable in enumerate(stable_mask):
        if is_stable:
            if start_idx is None:
                start_idx = i
            stable_count += 1
        else:
            # End of a stable run
            if start_idx is not None and stable_count >= min_stable_duration:
                if (i - start_idx) >= min_length:
                    start_time = data[time_col].iloc[start_idx]
                    end_time = data[time_col].iloc[i - 1]
                    if (end_time - start_time) >= min_segment_duration:
                        segments.append((start_time, end_time))
                    if len(segments) >= max_segments:
                        break
            start_idx = None
            stable_count = 0

    # Check if the last segment goes till the end of data
    if start_idx is not None and stable_count >= min_stable_duration and (len(data) - start_idx) >= min_length and len(segments) < max_segments:
        start_time = data[time_col].iloc[start_idx]
        end_time = data[time_col].iloc[-1]
        if (end_time - start_time) >= min_segment_duration:
            segments.append((start_time, end_time))

    return segments
