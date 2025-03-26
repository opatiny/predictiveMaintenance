import matplotlib.pyplot as plt

from utils.getFormattedSignalData import getFormattedSignalData


def addSeries(filePath: str, nbPoints: int = None) -> None:

    data = getFormattedSignalData(filePath)

    # pick how many points to plot
    # If nbPlots is None, plot all signals
    if nbPoints is None:
        nbPoints = data.shape[0]
    plotData = data.loc[:, :].head(nbPoints)

    # add series to current plot
    plt.plot(
        plotData.loc[:, "timeSeconds"], plotData.loc[:, "value"], "o-", markersize=3
    )
