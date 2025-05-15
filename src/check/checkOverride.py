import pandas as pd


def checkOverride(
    sample: pd.DataFrame, sampleName: str, debug: bool = False
) -> pd.DataFrame:
    """
    Verify if override signals were modified.

    Args:
        sample (pd.DataFrame): The sample to check.

    Returns:
        Dataframe indicating if override signals were modified, and corresponding indices.
    """
    overrideSignals = ["lrSigFeedRateOverride", "lrSigSpindleOverride"]

    modifiedSignals = []
    modIndices = [None] * len(overrideSignals)

    for signalName in range(len(overrideSignals)):
        # check signal exists
        if overrideSignals[signalName] not in sample.columns:
            modifiedSignals.append(None)
            continue

        signal = overrideSignals[signalName]
        modified = 0
        for i in range(len(sample[signal])):
            if sample.loc[i, signal] != 100:
                modified = 1
                modIndices[signalName] = i
                if debug:
                    print(f"Signal {signal} was modified in sample {sampleName}")
            if modified == 1:
                break
        if modified == 1:
            modifiedSignals.append(1)
        else:
            modifiedSignals.append(0)

    # put everything in a dataframe
    result = pd.DataFrame(
        {
            "feedRate": [modifiedSignals[0]],
            "spindle": [modifiedSignals[1]],
            "feedRateIndex": [modIndices[0]],
            "spindleIndex": [modIndices[1]],
        },
        index=[sampleName],
    )

    return result
