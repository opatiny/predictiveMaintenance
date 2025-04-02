# test the function pd.to_datetime
import pandas as pd


data = pd.Series(
    [
        "2025-02-03 08:40:13.000",
        "2025-02-03 08:40:14.000",
    ]
)


# test the function pd.to_datetime
format = "%Y-%m-%d %H:%M:%S.%f"
data = pd.to_datetime(data, format)
print(data)
