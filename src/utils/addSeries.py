import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize as normalizeSignal
from typing import TypedDict

from utils.getFormattedSignalData import getFormattedSignalData


class AddSeriesOptinons(TypedDict):
    """
    Options for the addSeries function.

    Attributes:

    nbPoints (int, optional): The number of points to plot. If None, all points will be plotted.
    normalize (bool, optional): Normalize the signal between -1 and 1.
    """

    nbPoints: int
    normalize: bool


def addSeries(filePath: str, options: AddSeriesOptinons = {}) -> None:

    nbPoints = options.get("nbPoints", None)
    normalize = options.get("normalize", False)
    min = options.get("min", 0)
    max = options.get("max", 1)

    data = getFormattedSignalData(filePath)

    if normalize:
        data.loc[:, "value"] = normalizeSignal(
            data.loc[:, "value"].values.reshape(-1, 1), axis=0, norm="max"
        ).reshape(-1)

    # pick how many points to plot
    # If nbPlots is None, plot all signals
    if nbPoints is None:
        nbPoints = data.shape[0]
    plotData = data.loc[:, :].head(nbPoints)

    # add series to current plot
    plt.plot(
        plotData.loc[:, "timeSeconds"], plotData.loc[:, "value"], "o-", markersize=3
    )
