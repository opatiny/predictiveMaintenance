import pandas as pd


def normalizeSignal(signal: pd.Series, min: float = 0, max: float = 1.0) -> pd.Series:
    """
    Normalize a signal between min and max values
    """
    # get the min and max values of the signal
    signalMin = signal.min()
    signalMax = signal.max()
    # normalize the signal
    signalNormalized = (signal - signalMin) / (signalMax - signalMin) * (
        max - min
    ) + min
    return signalNormalized
