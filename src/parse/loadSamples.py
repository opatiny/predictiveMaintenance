import os
import time
import pandas as pd

from parse.loadSample import loadSample


def loadSamples(path: str, debug: bool = False) -> tuple:
    """ "
    Load all samples from a folder.
    """
    # find samples names
    sampleNames = os.listdir(path)

    if debug:
        print("Number of samples to load: ", len(sampleNames))
        print("Sample names: ", sampleNames)

    # load all samples
    allSamples = []
    for sample in sampleNames:
        if debug:
            print("Loading sample: ", sample)
        start = time.time()
        data = loadSample(os.path.join(path, sample), debug)
        end = time.time()
        if debug:
            print("Time to load: ", end - start, " seconds")
        allSamples.append(data)

    return allSamples, sampleNames
