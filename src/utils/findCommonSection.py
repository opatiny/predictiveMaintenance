import pandas as pd


def findCommonSection(
    signal: pd.Series, reference: pd.Series, offset: int = 0, debug: bool = False
) -> pd.DataFrame:
    """
    Find the common section between the signal and reference. Signal and reference can have different lengths.

    Parameters
    ----------
    signal (pd.Series): The signal data.
    reference (pd.Series): The reference data.
    offset (float): The x offset to align the signal on the reference.

    Returns
    -------
    pd.DataFrame: The common section between the signal and reference.
    """
    # find start and end indices for signal and reference
    sigStart = max(0, -offset)
    refStart = max(0, offset)
    sigEnd = min(len(signal) - 1, len(reference) - offset - 1)
    refEnd = min(len(reference) - 1, len(signal) + offset - 1)
    if debug:
        print(
            f"sigStart: {sigStart}, refStart: {refStart}, sigEnd: {sigEnd}, refEnd: {refEnd}"
        )

    # ignore index
    return pd.DataFrame(
        {
            "signal": signal[sigStart:sigEnd].reset_index(drop=True),
            "reference": reference[refStart:refEnd].reset_index(drop=True),
        },
    )
