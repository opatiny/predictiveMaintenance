import matplotlib.pyplot as plt
import pandas as pd
import math

from utils import Utils

folderPath = "data/Machine#1_Mecatis/Warmup_Mecatis_03_02_25/"
filename = "stSigAxCurrentB.csv"
filePath = folderPath + filename

# Load data from csv file
data = pd.read_csv(
    filePath, sep=";", header=None
)  # use names=["time", "value"] to add column names

# sort data by time
data = data.sort_values(by=0)

# convert time to seconds from beginning of array
data.loc[:, 0] = Utils.getNormalizedTime(data.loc[:, 0])

# pick how many points to plot
nbPoints = math.floor(data.shape[0] / 10)
plotData = data.loc[:, :].head(nbPoints)

# get y label
yLabel = Utils.getYLabel(filename)

# Plot data
plt.plot(plotData.loc[:, 0], plotData.loc[:, 1], "ro-", markersize=3)
plt.title(filePath)
plt.xlabel("Time [s]")
plt.ylabel(yLabel)
plt.grid(True)
plt.show()

# Close all plots
plt.close("all")
