import os
import time
import pandas as pd

from parse.loadSample import loadSample


def loadSamples(path: str, currentUnit: str = "A", debug: bool = False) -> tuple:
    """
    Load all samples from a folder.

    Args:
        path (str): Path to the folder containing the samples.
        debug (bool): If True, print debug information.
    Returns:
        tuple: A tuple containing a list of all samples in pd.DataFrame format and a list of sample names.
    """
    # find samples names
    sampleNames = os.listdir(path)

    machineName = path.split("/")[-1]

    if debug:
        print("Current machine: ", machineName)

    if debug:
        print("Number of samples to load: ", len(sampleNames))
        print("Sample names: ", sampleNames)

    # load all samples
    allSamples = []
    names = []
    for sample in sampleNames:
        if debug:
            print("Loading sample: ", sample)
        start = time.time()
        data = loadSample(os.path.join(path, sample), currentUnit=currentUnit)
        end = time.time()
        if debug:
            print("Time to load: ", round(end - start, 2), " seconds")
        allSamples.append(data)

        # append machine name to the sample name
        fileName = sample.split(".")[0]  # remove the extension if it exists
        names.append(f"{machineName}_{fileName}")

    return allSamples, names
