from matplotlib import pyplot as plt
import pandas as pd


def plotSegmentsManySamples(
    segmentedSamples: list[list[pd.DataFrame]],
    xSignal: str = "timeSeconds",
    ySignal: list[str] = ["current"],
    nbPoints: int = None,
    title="Spindle current",
    xlabel: str = "Time (s)",
    ylabel: str = "Current (A)",
    legend: list[str] = [],
) -> None:
    """
    Plot the segments of a signal for multiple samples.
    The segments are plotted in a 2x3 grid.

    Parameters
    ----------
    segmentedSamples (list[list[pd.DataFrame]]): List of dataframes of the segments for multiple samples.
    xSignal (str): The name of the x signal.
    ySignals (str): The name of the y signal to plot.
    nbPoints (int): The number of points to plot. If None, all points are plotted.
    title (str): The title of the plot.
    xlabel (str): The label of the x-axis.
    ylabel (str)]: The label of the y-axis.

    Returns
    -------
    None
    """

    nbSegments = len(segmentedSamples[0])
    if nbSegments != 6:
        print("Warning: the number of segments is not 6. The plot may be incorrect.")

    nbColumns = 2
    nbRows = 3

    plt.figure()
    fig, axs = plt.subplots(nbRows, nbColumns, figsize=(12, 8))
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle(title)

    for i in range(nbSegments):
        x = segments[i].loc[:, xSignal]
        for j in range(len(ySignals)):

            ySignal = ySignals[j]
            y = segments[i].loc[:, ySignal]

            colIndex = i % nbColumns
            rowIndex = i // nbColumns

            axs[rowIndex, colIndex].plot(x[:nbPoints], y[:nbPoints], "o-", markersize=3)
        axs[rowIndex, colIndex].set_xlabel(xlabel)
        pointsToPlot = len(x)
        if nbPoints != None:
            pointsToPlot = min(nbPoints, len(x))
        axs[rowIndex, colIndex].set_ylabel(ylabel)
        axs[rowIndex, colIndex].set_title(
            "Segment " + str(i + 1) + " (" + str(pointsToPlot) + " points)"
        )
        if len(legend) > 0:
            axs[rowIndex, colIndex].legend(legend)
        axs[rowIndex, colIndex].grid()

    plt.show()
