import os
from pathlib import Path
import matplotlib.pyplot as plt

from formatSampleData import formatSampleData


folderPath = "data/Machine#1_Mecatis/Warmup_Mecatis_03_02_25/"
data = formatSampleData(folderPath, debug=True)

# save data to csv
data.to_csv("data.csv", index=False)
