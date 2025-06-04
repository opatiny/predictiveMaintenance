# Predictive maintenance project

## Context

Use warm-up data of micro5 milling machines in order to identify the machine the sample comes from. Implement normalization functions to ensure the uniformity of the data.

## Initial objectives

1. Cluster data in order to attribute new data to the correct machine
2. Create a transformation procedure in order to normalize a machines data into a reference framework

## Repository structure

### Branches

The developments of the different students who participated to the project are placed in different branches of this repository. To access some of the code, you should inspect the other branches.

### `main` branch

The `main` branch contains code for visualization of the data, checking that the data is valid, normalizing the data, and a prototype of temperature correction for the spindle current.

The `main` branch has the following structure:

- `data`: contains all of the samples from the different machines
- `docs`: weekly readmes of advancements made and other documentation
- `src`: main folder containing the code
- `results`: folder used to output results from various functions

The `src` folder itself contains the following subfolders:

- `check`: control functions to verify that the data is suitable for further analysis
- `notebooks`: Jupyter notebooks, mainly to test the temperature correction procedure
- `parse`: functions to load and normalize sample data, be it from `.csv` or `.parquet`files
- `plot`: various functions to plot the data
- `signalProcessing`: functions to modify a signal
- `temperatureCorrection`: all code relative to the temperature correction prototype
- `tests`: scripts that allow to call the other functions in order to test if they work properly. The code in this folder is a good starting point to understand how the rest of the code works and is organised.
- `utils`: All utilities functions

## Data folder structure

Empty

## Running unit tests

This project contains unit tests for some of the functions. All unit tests are placed in the subfolders named `__tests__`. To run the unit tests, just run the python test file as you would any other file.
