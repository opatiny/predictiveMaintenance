# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd
import time

from plot.plotSignal import plotSignal

from typing import TypedDict


class PlotSignalsOptions(TypedDict):
    """
    Options for the plotSignals function.

    Attributes:

    nbPlots (int, optional): The number of files to process. If None, all files in the folder will be plotted.
    nbPoints (int, optional): The number of points from the data to plot. If None, all points will be plotted.
    debug (bool, optional): Print debug information.
    filterPlots (bool, optional): Only keep the signals with useful == 1 in the signalsDescription.csv file.
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
    options (PlotSignalsOptions): The options for the plotSignals function.

    Returns:
    None
    """
    nbPlots = options.get("nbPlots", None)
    nbPoints = options.get("nbPoints", None)
    debug = options.get("debug", False)
    filterPlots = options.get("filterPlots", False)

    dataFolderName = dataPath.split("/")[-1]
    print(dataFolderName)

    saveFolderPath = savePath + dataFolderName

    # Create a new folder to save plots
    if not os.path.exists(saveFolderPath):
        os.makedirs(saveFolderPath)

    # Get all files in the folder
    files = os.listdir(dataPath)

    # Read signals descriptions
    fileAbsPath = os.path.abspath(__file__)
    fileDir = os.path.dirname(fileAbsPath)
    infoPath = fileDir + "/../../data/signalsDescription.csv"
    signalsInformation = pd.read_csv(infoPath, sep=",")

    # only keep the interesting signals from the folder

    usefulSignals = signalsInformation[signalsInformation["useful"] == 1]

    if filterPlots:
        files = [file for file in files if file in usefulSignals["name"].values]

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
            print("Plotting file ", i, "/", nbPlots)

        # compute time to run plotSignal
        start_time = time.time()
        plotSignal(dataPath + "/" + file + ".csv", nbPoints, debug)
        end_time = time.time()

        if debug:
            print(f"Time to plot signal: {end_time - start_time:.6f} seconds")

        # Save the plot
        start_time = time.time()
        # todo: very slow when using svg format
        plt.savefig(saveFolderPath + "/" + file + ".png", format="png")
        end_time = time.time()

        if debug:
            print(f"Time to save figure: {end_time - start_time:.6f} seconds")

    if debug:
        print("Plots saved in ", saveFolderPath)
