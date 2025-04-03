import pandas as pd
import polars as pl

from utils import Utils


def loadParquetSample(path: str, debug: bool = False) -> pd.DataFrame:
    """ "
    Load a sample in parquet format and return a pandas dataframe.
    Removes duplicates and normalizes time.
    Removes columns that are full of NaN.
    """

    # load all data
    data = pl.read_parquet(path)
    # convert to pandas dataframe
    data = data.to_pandas()

    if debug:
        print("original data: ", data.shape)
        print(data.head())

    # normalize time
    data["time"] = Utils.normalizeParquetTime(data["time"])

    # delete columns that are full of NaN
    data.dropna(axis=1, how="all", inplace=True)

    # remove duplicates
    # tricky because the values alternate from one signal to another
    first = Utils.removeDuplicatesFromParquet(data, keep="first", debug=debug)
    first.dropna(axis=1, how="any", inplace=True)
    last = Utils.removeDuplicatesFromParquet(data, keep="last", debug=debug)
    last.dropna(axis=1, how="any", inplace=True)

    # merge the two dataframes along columns
    data = pd.concat([first, last], axis=1)

    if debug:
        print("normalized data: ", data.shape)
        print(data.head())

    return data
