import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(
    "results/formattedData.csv",
    sep=";",
)

# plot some data
plt.plot(data["timeSeconds"], data["lrSigSpindleTemp"], "o-", markersize=3)
plt.plot(data["timeSeconds"], data["stSigAxCurrentS"], "o-", markersize=3)
plt.xlabel("Time (s)")
plt.ylabel("Data")
plt.title("Formatted Data")
plt.legend(["lrSigSpindleTemp", "stSigAxCurrentS"])
plt.grid()
plt.show()
