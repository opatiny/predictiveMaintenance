# Predictive maintenance project

## Context

Use warm-up data of micro5 milling machines in order to identify the current machine, and create a transformation matrix to adapt tools to the given machine.

## Objectives

1. Cluster data in order to attribute new data to the correct machine
2. Create a transformation matrix in order to normalize a machines data into a reference framework

## Running unit tests

Just run the python test file as you would any other file.

## Time stamps

Time stamps of the csv samples are in Microsoft filetime format!!

"The FILETIME structure is a 64-bit value that represents the number of 100-nanosecond intervals that have elapsed since January 1, 1601, Coordinated Universal Time (UTC)."

## Signals that look interesting

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

## Implementation

### Data frames

Data frames allow to store table like data. We have two main libraries that handle dataframes: `pandas` and `polars`. Apparently, `polars` is a lot faster though.

https://blog.jetbrains.com/pycharm/2024/07/polars-vs-pandas/

### Parsing string dates

- initially wanted to use `datetime.strptime(date, format)`, but it's super slow (several minutes for 3e6 values...)
- alternatives:
  - `pandas.to_datetime()`
  - `pendulum`

## Various notes

- does knowing the temperature allow us to make some kind of compensation on the data?
