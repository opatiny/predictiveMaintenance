# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd


# Function to plot signals
def plotSignals(folderPath, savePath, nbPlots):
    # Create a new folder to save plots
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Get all files in the folder
    files = os.listdir(folderPath)

    # If nbPlots is None, plot all signals
    if nbPlots is None:
        nbPlots = len(files)

    files = sorted(files)[:nbPlots]

    print("Files to plot: ", files)

    # Loop through all files
    for file in files:
        # Read the file
        data = pd.read_csv(
            folderPath + "/" + file, header=None, sep=";", index_col=False
        )

        # Convert time to seconds
        data[0] = (data[0] - data[0][0]) / 1e9

        # Get the signal name
        signal_name = file.split(".")[0]

        # Plot the signal
        plt.figure()
        plt.plot(data[0], data[1], label=signal_name)
        plt.title(signal_name)
        plt.xlabel("Time [s]")
        plt.ylabel("Value")
        plt.grid()
        plt.savefig(savePath + "/" + signal_name + ".svg", format="svg")
        plt.close()
