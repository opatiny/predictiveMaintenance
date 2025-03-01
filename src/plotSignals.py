# Plot all signals from a folder and save plots in a new folder

import os
import matplotlib.pyplot as plt
import pandas as pd


# Function to plot signals
def plotSignals(folderPath, savePath):
    # Create a new folder to save plots
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Get all files in the folder
    files = os.listdir(folderPath)
    files = sorted(files)[:3]

    print(files)

    # Loop through all files
    for file in files:
        # Read the file
        data = pd.read_csv(folderPath + "/" + file, header=None)

        print(data)

        # Get the signal name
        signal_name = file.split(".")[0]

        # Plot the signal
        plt.figure()
        plt.plot(data)
        plt.title(signal_name)
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.savefig(savePath + "/" + signal_name + ".svg", format="svg")
        plt.close()
