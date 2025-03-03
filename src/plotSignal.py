import matplotlib.pyplot as plt
import pandas as pd

from utils import Utils

folderPath = "data/Warmup_Mecatis_03_02_25/"
filename = "stSigAxPosACSB.csv"
filePath = folderPath + filename

# Load data from csv file
data = pd.read_csv(filePath, sep=";", header=None)

print("sorting data")

# sort data by time
data = data.sort_values(by=0)

print(data[:][:100])

print(data[0])

print("min time: ", data[0].min())

data[0] = Utils.normalizeTime(data[0])

print("Nb points: ", len(data[0]))

print(data[:][:100])

# Plot data
plt.plot(data[0], data[1], "ro-")
plt.title(filePath)
plt.xlabel("Time [s]")
plt.ylabel("Value")
plt.grid(True)
plt.show()
plt.close("all")

# Close all plots
plt.close("all")
