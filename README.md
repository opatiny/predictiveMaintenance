# Predictive maintenance project

## Context

Use warm-up data of micro5 milling machines in order to identify the current machine, and create a transformation matrix to adapt tools to the given machine.

## Objectives

1. Cluster data in order to attribute new data to the correct machine
2. Create a transformation matrix in order to normalize a machines data into a reference framework

## Running unit tests

Just run the python test file as you would any other file.

## Data format

### Time stamps

#### In `.csv` files

Time stamps of the csv samples are in Microsoft filetime format!!

"The FILETIME structure is a 64-bit value that represents the number of 100-nanosecond intervals that have elapsed since January 1, 1601, Coordinated Universal Time (UTC)."

#### In `.parquet` files

`time` column contains time as date strings in ISO 8601.

https://fr.wikipedia.org/wiki/ISO_8601

### Signals that look interesting

- spindle temperature: lrSigSpindleTemp
- axes currents
  - stSigAxCurrentB
  - stSigAxCurrentS
  - stSigAxCurrentX
  - stSigAxCurrentY
  - stSigAxCurrentZ
- following error signals
- axes positions
- axes velocities
- spindle power: stSigPowerMotS
- commands:
  - stSigSpindleVelocity
  - stSigOperation

### Positions

- ACS: tool reference frame
- MCS: machine reference frame

### Overrides

Some of the signals are overrides of the user on the target value defined inside the program. This value is expressed as a percentage of the target value. For example, an override of 150% means that the current value is 1.5 times greater than the one in the program. If there is no user override, the override variables are at 100.

## Implementation

### Data frames

Data frames allow to store table like data. We have two main libraries that handle dataframes: `pandas` and `polars`. Apparently, `polars` is a lot faster though.

https://blog.jetbrains.com/pycharm/2024/07/polars-vs-pandas/

### Parsing string dates

- initially wanted to use `datetime.strptime(date, format)`, but it's super slow (several minutes for 3e6 values...)
- alternatives:
  - `pandas.to_datetime()`
  - `pendulum`
  - `isotime`

## Various notes

- does knowing the temperature allow us to make some kind of compensation on the data?
