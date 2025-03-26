import matplotlib.pyplot as plt
import pandas as pd

from utils.getFormattedSignalData import getFormattedSignalData
from utils import Utils


def plotSignal(filePath: str, nbPoints: int = None, debug: bool = False) -> None:
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
    data = getFormattedSignalData(filePath, debug)

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
        plotData.loc[:, "timeSeconds"], plotData.loc[:, "value"], "o-", markersize=3
    )
    plt.title(signalsFolderName + " - " + filename)
    plt.xlabel("Time [s]")
    plt.ylabel(yLabel)
    plt.grid(True)
