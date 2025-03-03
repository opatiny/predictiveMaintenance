# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd


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

    # If nbPlots is None, plot all signals
    if nbPlots is None:
        nbPlots = len(files)

    files = sorted(files)[:nbPlots]

    print("Files to plot: ", files)

    # Loop through all files
    for file in files:
        # Read the file
        data = pd.read_csv(dataPath + "/" + file, header=None, sep=";", index_col=False)

        # Convert time to seconds
        data[0] = (data[0] - data[0][0]) / 1e9

        # Get the signal name
        signal_name = file.split(".")[0]

        # Plot the signal
        plt.figure()
        plt.plot(data[0], data[1], label=signal_name)
        plt.title(dataFolderName + ": " + signal_name)
        plt.xlabel("Time [s]")
        plt.ylabel("Value")
        plt.grid()
        plt.savefig(saveFolderPath + "/" + signal_name + ".svg", format="svg")
        plt.close()
