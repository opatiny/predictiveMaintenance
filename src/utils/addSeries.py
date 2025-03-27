import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize as normalizeSignal
from typing import TypedDict

from utils.getFormattedSignalData import getFormattedSignalData


class AddSeriesOptions(TypedDict):
    """
    Options for the addSeries function.

    Attributes:

    nbPoints (int, optional): The number of points to plot. If None, all points will be plotted.
    normalize (bool, optional): Normalize the signal between -1 and 1.
    """

    nbPoints: int
    normalize: bool
    debug: bool


def addSeries(filePath: str, options: AddSeriesOptions = {}) -> None:

    nbPoints = options.get("nbPoints", None)
    normalize = options.get("normalize", False)
    debug = options.get("debug", False)

    data = getFormattedSignalData(filePath, normalize, debug)

    # pick how many points to plot
    # If nbPlots is None, plot all signals
    if nbPoints is None:
        nbPoints = data.shape[0]
    plotData = data.loc[:, :].head(nbPoints)

    # add series to current plot
    plt.plot(
        plotData.loc[:, "timeSeconds"], plotData.loc[:, "value"], "o-", markersize=3
    )
