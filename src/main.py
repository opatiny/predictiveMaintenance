import os
from pathlib import Path
import matplotlib.pyplot as plt

from plotSignals import plotSignals
from plotSignal import plotSignal


plotSignals(
    "data/Machine#1_Mecatis/Warmup_Mecatis_03_02_25",
    "src/plots/",
    {"debug": True, "filterPlots": False},
)


# get the current folder path
# currentPath = Path(__file__).resolve().parent
# print(currentPath)

# relFolderPath = "../data/Machine#1_Mecatis/Warmup_Mecatis_03_02_25/"
# fileName = "stSigAxCurrentB.csv"

# # concanetating the path
# filePath = str(currentPath / relFolderPath / fileName)
# print("filePath: ", filePath)
# plotSignal(filePath)
# plt.show()

# # Close all plots
# plt.close("all")
