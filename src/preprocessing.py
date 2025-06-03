import os
import numpy as np
import pandas as pd
from typing import Optional

def detect_sampling_rate(file_path: str) -> int:
    """
    Detect the sampling rate based on keywords found in the filename.

    Parameters:
    ----------
    file_path : str
        Path to the data file, used to extract filename for detection.

    Returns:
    -------
    int
        Sampling rate in Hz inferred from filename keywords.
        Defaults to 1000 Hz if no keyword matched.
    
    Notes:
    -----
    This function assumes specific keywords in the filename
    to infer the data acquisition frequency.
    """
    file_name = os.path.basename(file_path).casefold()

    if "mill" in file_name:
        return 2000
    elif "mecatis" in file_name:
        return 1250
    elif "locle" in file_name:
        return 1000
    # Default sampling rate
    return 1000


def adjust_signal_scale(
    data: pd.DataFrame,
    file_path: str,
    signal_column: str = 'stSigSpindleIndicator'
) -> pd.DataFrame:
    """
    Adjust the spindle current signal values to ensure consistent units.

    Parameters:
    ----------
    data : pd.DataFrame
        Input data containing the spindle signal.
    file_path : str
        Path of the data file, used to detect the source/type.
    signal_column : str, optional
        Name of the spindle current signal column, by default 'stSigSpindleIndicator'

    Returns:
    -------
    pd.DataFrame
        Modified dataframe with adjusted signal values where applicable.
    
    Notes:
    -----
    - For 'mecatis' data files, signal units are converted by dividing by 1000
      to convert from mA to A (Amperes).
    """
    file_name = os.path.basename(file_path).casefold()

    if 'mecatis' in file_name:
        if signal_column in data.columns:
            data = data.copy()
            data[signal_column] = data[signal_column] / 1000.0
        else:
            raise KeyError(f"Signal column '{signal_column}' not found in data for file {file_path}")

    return data


def ensure_time_column(
    data: pd.DataFrame,
    original_col: str = 'time',
    target_col: str = 'timeSeconds'
) -> pd.DataFrame:
    """
    Ensure that a standard time column is present in the DataFrame.

    Parameters:
    ----------
    data : pd.DataFrame
        Input data with time columns.
    original_col : str, optional
        Original time column name to rename from, by default 'time'.
    target_col : str, optional
        Target standard time column name, by default 'timeSeconds'.

    Returns:
    -------
    pd.DataFrame
        DataFrame with time column renamed as needed.
    
    Notes:
    -----
    - If `target_col` already exists, the data is returned unchanged.
    - If `original_col` exists but `target_col` does not, `original_col` is renamed.
    """
    if target_col in data.columns:
        return data

    if original_col in data.columns:
        return data.rename(columns={original_col: target_col})

    raise KeyError(f"Neither '{target_col}' nor '{original_col}' columns found in data.")


def remove_time_gaps(
    data: pd.DataFrame,
    time_column: str = 'timeSeconds',
    max_gap: Optional[float] = None
) -> pd.DataFrame:
    """
    Create a continuous time vector by correcting large time gaps.

    Parameters:
    ----------
    data : pd.DataFrame
        Input dataframe containing time column.
    time_column : str, optional
        Name of the time column to correct, by default 'timeSeconds'.
    max_gap : float or None, optional
        Expected nominal time difference between samples (default=None).
        If None, uses median of time differences as nominal dt.

    Returns:
    -------
    pd.DataFrame
        DataFrame with an additional column '{time_column}_nogap'
        where large time jumps are corrected to create a continuous timeline.

    Notes:
    -----
    - Identifies large gaps as intervals greater than 1.5 * nominal dt.
    - Subtracts cumulative excess gap time to "flatten" the time vector.
    """
    if time_column not in data.columns:
        raise KeyError(f"Time column '{time_column}' not found in dataframe.")

    df = data.copy()
    times = df[time_column].values

    if len(times) < 2:
        # Not enough data to detect gaps
        df[time_column + '_nogap'] = times
        return df

    diffs = np.diff(times)
    dt_nominal = max_gap if max_gap is not None else np.median(diffs)
    jump_correction = np.zeros(len(times))

    for i in range(1, len(times)):
        if diffs[i - 1] > dt_nominal * 1.5:
            # Large gap detected, adjust subsequent times
            jump_correction[i:] += diffs[i - 1] - dt_nominal

    df[time_column + '_nogap'] = times - jump_correction

    return df
