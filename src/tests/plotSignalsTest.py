import os
import sys

fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from plot.plotSignals import plotSignals

plotSignals(
    "data/Mecatis/03_02_25",
    "results/",
    {"debug": True, "filterPlots": False, "nbPlots": None},
)
