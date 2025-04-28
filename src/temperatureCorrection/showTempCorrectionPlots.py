from matplotlib import pyplot as plt


def showTempCorrectionPlots(data: list, sampleNames: list) -> None:
    """
    Show the temperature and current plots for the given data.

    Parameters
    ----------
    data (list[pd.DataFrame]): List of dataframes containing the time, temperature and current data.
    sampleNames (list[str]): List of sample names corresponding to the data.
    """
    # plot temperature versus time
    plt.figure()
    for i in range(len(data)):
        plt.plot(
            data[i]["timeSeconds"],
            data[i]["temperature"],
            "o-",
            markersize=3,
            label=sampleNames[i],
        )
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.title("Spindle temperature")
    plt.legend()
    plt.grid()
    plt.show()

    # plot current versus time
    plt.figure()
    for i in range(len(data)):
        plt.plot(
            data[i]["timeSeconds"],
            data[i]["current"],
            "o-",
            markersize=3,
            label=sampleNames[i],
        )
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.title("Spindle current")
    plt.legend()
    plt.grid()
    plt.show()

    # plot current versus temperature
    plt.figure()
    for i in range(len(data)):
        plt.plot(
            data[i]["temperature"],
            data[i]["current"],
            "o-",
            markersize=3,
            label=sampleNames[i],
        )
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Current (A)")
    plt.title("Spindle current VS temperature")
    plt.legend()
    plt.grid()
    plt.show()
