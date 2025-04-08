# Project intermediate results (2025.03.10)

## changelog

- finished `loadSamples` function, which loads all samples from a machine and processes them (samples can be either csv or parquet)
- finished `saveNormalizedSamples` which saves formatted data into .parquet files so that they can be reused later on

## various notes

- processing the whole signal versus processing each segment separately
- we are trying to remove biases: temperature difference, axes that aren't working on a machine, etc
