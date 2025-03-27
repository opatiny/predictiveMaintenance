import os
import sys

fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from plotSignals import plotSignals


plotSignals(
    "data/mecatis/Warmup_Mecatis_05_02_25",
    "src/plots/mecatis/",
    {"debug": True, "filterPlots": False},
)
