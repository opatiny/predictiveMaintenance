import pandas as pd
import os
import sys

# Add the current folder to the path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import Utils

def getFormattedSignalData(filePath: str) -> pd.DataFrame:
    """
    Load and format signal data from a CSV file.

    Parameters:
    filePath (str): The path to the CSV file containing the signal data.

    Returns:
    pd.DataFrame: A DataFrame with formatted signal data.
    """
    # Load data from CSV file
    data = pd.read_csv(filePath, sep=";", header=None, names=["timestamp", "value"])

    # Sort data by timestamp
    data = data.sort_values(by="timestamp")

    # Remove duplicate timestamps, keeping the first occurrence
    data = data.drop_duplicates(subset="timestamp", keep="first")

    # Convert time to seconds from the beginning of the array
    data["timeSeconds"] = Utils.getNormalizedTime(data["timestamp"])

    # Select only the desired columns
    formattedData = data[["timeSeconds", "value"]]

    return formattedData
