# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd

from utils import Utils
from plotSignal import plotSignal

from typing import TypedDict


class PlotSignalsOptions(TypedDict):
    """
    Options for the plotSignals function.

    Attributes:

    nbPlots (int, optional): The number of files to process. If None, all files in the folder will be plotted.
    nbPoints (int, optional): The number of points from the data to plot. If None, all points will be plotted.
    debug (bool, optional): Print debug information.
    filterPlots (bool, optional): Filter the signals to plot.
    """

    nbPlots: str
    nbPoints: int
    debug: bool
    filterPlots: bool


# Function to plot signals
def plotSignals(dataPath: str, savePath: str, options: PlotSignalsOptions = {}) -> None:
    """
    Plot all signals from a folder and save plots in a new folder.

    Parameters:
    dataPath (str): The path to the folder containing the signal files.
    savePath (str): The path to the folder where the plots will be saved. The function automatically creates a new folder with the same name as the data folder.
    options (Options): The options for the plotSignals function.

    Returns:
    None
    """
    nbPlots = options.get("nbPlots", None)
    nbPoints = options.get("nbPoints", None)
    debug = options.get("debug", False)
    filterPltos = options.get("filterPlots", False)

    dataFolderName = dataPath.split("/")[-1]
    print(dataFolderName)

    saveFolderPath = savePath + dataFolderName

    # Create a new folder to save plots
    if not os.path.exists(saveFolderPath):
        os.makedirs(saveFolderPath)

    # Get all files in the folder
    files = os.listdir(dataPath)

    # Read signals descriptions
    signalsInformation = pd.read_csv("data/signalsDescription.csv", sep=",")

    # only keep the interesting signals from the folder
    files = [file for file in files if file in signalsInformation["fileName"].values]

    # If nbPlots is None, plot all signals
    if nbPlots is None:
        nbPlots = len(files)

    files = sorted(files)[:nbPlots]

    print("Files to plot: ", files)

    i = 0

    # Loop through files
    for file in files:
        i += 1
        if debug:
            print("Plotting file ", i, " / ", nbPlots)

        plotSignal(dataPath + "/" + file, nbPoints)

        # Save the plot
        fileName = file.split(".")[0]
        plt.savefig(saveFolderPath + "/" + fileName + ".svg", format="svg")
        plt.close()
