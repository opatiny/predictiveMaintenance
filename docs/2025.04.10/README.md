# Project intermediate results (2025.03.10)

## changelog

- finished `loadSamples` function, which loads all samples from a machine and processes them (samples can be either csv or parquet)
- finished `saveNormalizedSamples` which saves formatted data into .parquet files so that they can be reused later on
- reused the segmentation function written by Gael
- started working on temperature compensation

## various notes

- processing the whole signal versus processing each segment separately
- we are trying to remove biases: temperature difference, axes that aren't working on a machine, etc
- we can only base ourselves on the signals that are present in all the samples -> we must have a guarantee that at least some of the signals are present in **all** the samples
