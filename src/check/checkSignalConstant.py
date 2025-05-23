import pandas as pd


def checkSignalConstant(signal: pd.Series, debug: bool = False) -> bool:
    """
    Check if a signal is constant or not.
    A signal is considered constant if it has the same value for all points.

    Args:
        sample (pd.Series): The signal to check.

    Returns:
        bool: True if the signal is constant, False otherwise.
    """
    # check if the signal is constant
    if signal.nunique() == 1:
        if debug:
            print("Signal is constant")
        return True
    else:

        # check if the signal is constant but contains NaN
        if signal.dropna().nunique() == 1:
            if debug:
                print("Signal is constant but contains NaN")
            return False

        if debug:
            print("Signal is not constant")

        # check at which index the signal changes
        for i in range(len(signal) - 1):
            if signal[i] != signal[i + 1]:
                if debug:
                    print(f"Signal changes at index {i}")
                return False

        return False
