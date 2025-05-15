import pandas as pd


def plotFrequency(time: pd.Series, sampleName: str = "sample") -> None:
    """
    Plot the frequency of the time series.

    Parameters
    ----------
    time (pd.Series): The time series data.

    Returns
    -------
    None
    """
    import matplotlib.pyplot as plt

    # Compute the difference between consecutive time points
    diff = time.diff().dropna()

    # check if diff contains some zeros
    if diff.isin([0]).any():
        Warning("Signal contains duplicate time stamps")

    # replace zeros with NaN
    diff = diff.replace(0, pd.NA)

    frequency = 1 / diff

    # Plot the frequency of the time series
    plt.figure()
    plt.plot(frequency, "o-", markersize=3)
    plt.title(sampleName + ": Sampling frequency")
    plt.xlabel("Index")
    plt.ylabel("Frequency [Hz]")
    plt.grid()
    plt.show()
