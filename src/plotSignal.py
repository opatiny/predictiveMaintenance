import matplotlib.pyplot as plt
import pandas as pd
import math

from utils import Utils


def plotSignal(filePath: str, nbPoints: int = None) -> None:
    """
    Plot a signal from a csv file.

    Parameters:
    filePath (str): The path to the csv file containing the signal.
    nbPoints (int, optional): The number of points to plot. If None, all points will be plotted.

    Returns:
    None
    """

    # Get filename
    signalsFolderName = filePath.split("/")[-2]
    filename = filePath.split("/")[-1]

    # Load data from csv file
    data = pd.read_csv(
        filePath, sep=";", header=None, names=["timestamp", "value"]
    )  # use names=["time", "value"] to add column names

    # sort data by time
    data = data.sort_values(by="timestamp")

    # convert time to seconds from beginning of array
    data.loc[:, "timeSeconds"] = Utils.getNormalizedTime(data.loc[:, "timestamp"])

    # pick how many points to plot
    # If nbPlots is None, plot all signals
    if nbPoints is None:
        nbPoints = data.shape[0]
    plotData = data.loc[:, :].head(nbPoints)

    # get y label
    yLabel = Utils.getYLabel(filename)

    # Plot data
    plt.figure()
    plt.plot(
        plotData.loc[:, "timeSeconds"], plotData.loc[:, "value"], "ro-", markersize=3
    )
    plt.title(signalsFolderName + "  " + filename)
    plt.xlabel("Time [s]")
    plt.ylabel(yLabel)
    plt.grid(True)
