# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd

from utils import Utils


# Function to plot signals
def plotSignals(dataPath: str, savePath: str, nbPlots: int = None) -> None:
    """
    Plot all signals from a folder and save plots in a new folder.

    Parameters:
    dataPath (str): The path to the folder containing the signal files.
    savePath (str): The path to the folder where the plots will be saved. The function automatically creates a new folder with the same name as the data folder.
    nbPlots (int, optional): The number of files to process. If None, all files in the folder will be plotted.

    Returns:
    None
    """

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

    # Loop through files
    for file in files:
        # Read the file
        data = pd.read_csv(dataPath + "/" + file, header=None, sep=";", index_col=False)

        # Convert time to seconds
        data.loc[0] = Utils.getNormalizedTime(data.loc[0])

        # Get the signal name
        signalName = file.split(".")[0]

        signalIndex = signalsInformation[signalsInformation["fileName"] == file].index[
            0
        ]

        print(signalIndex)

        signalDescription = signalsInformation.loc[signalIndex, "description"]
        signalUnit = signalsInformation.loc[signalIndex, "unit"]

        yLabel = signalDescription + " [" + signalUnit + "]"

        # Plot the signal
        plt.figure()
        plt.plot(data[0], data[1], label=signalName)
        plt.title(dataFolderName + ": " + signalName)
        plt.xlabel("Time [s]")
        plt.ylabel(yLabel)
        plt.grid()
        plt.savefig(saveFolderPath + "/" + signalName + ".svg", format="svg")
        plt.close()
