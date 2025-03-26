import os
import sys

fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from plotSignals import plotSignals

plotSignals(
    "data/Mecatis/Warmup_Mecatis_03_02_25",
    "src/plots/",
    {"debug": True, "filterPlots": True, "nbPlots": 2},
)
