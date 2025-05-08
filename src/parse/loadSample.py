from matplotlib import path
import pandas as pd

from parse.loadParquetSample import loadParquetSample
from parse.loadCsvSample import loadCsvSample


def loadSample(path: str, currentUnit: str = "A", debug: bool = False) -> pd.DataFrame:
    """
    Load a sample in parquet or csv format and return a pandas dataframe.

    Parameters
    ----------
    path : str
        The path to the sample file or folder.
    debug : bool, optional
        If True, print debug information. Default is False.
    """
    # check if sample is parquet or csv
    if path.endswith(".parquet"):
        data = loadParquetSample(path, currentUnit, debug)
    else:
        data = loadCsvSample(path, currentUnit, debug)

    return data
