import numpy as np
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

    # remove columns that are full of NaN
    data = data.dropna(axis=1, how="all")

    # create correct time series
    correctTime = data["time"].drop_duplicates()
    correctTime = correctTime.reset_index(drop=True)

    nbPoints = len(correctTime)

    finalData = pd.DataFrame()
    finalData["time"] = correctTime

    # format each signal
    for col in data.columns:
        if col != "time":
            # remove duplicates
            signalWithoutNan = data[col].dropna()

            # interpolate if points are missing
            if len(signalWithoutNan) != nbPoints:
                timeWithoutNan = data["time"][signalWithoutNan.index]

                correctSignal = np.interp(
                    correctTime,
                    timeWithoutNan,
                    signalWithoutNan,
                )

                # add to final data
                finalData[col] = correctSignal
            else:
                # add to final data
                finalData[col] = signalWithoutNan

    if debug:
        print("normalized data: ", finalData.shape)
        print(finalData.head())

    # reset index
    finalData = finalData.reset_index(drop=True)

    return finalData
