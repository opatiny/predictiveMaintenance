import pandas as pd
import polars as pl

from utils import Utils


def loadParquetSample(path: str, debug: bool = False) -> pd.DataFrame:
    """ "
    Load a sample in parquet format and return a pandas dataframe.
    Removes duplicates and normalizes time.
    """
    # load all data
    data = pl.read_parquet(path)

    if debug:
        print("data: ", data.shape)
        print(data.head())

    # normalize time
    nulls = data["time"].is_null().any()
    print("nulls: ", nulls)
    data["time"] = Utils.normalizeParquetTime(data["time"])

    print("caca")

    return data
