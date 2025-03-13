# Predictive maintenance project

## Context

Use warm-up data of micro5 milling machines in order to identify the current machine, and create a transformation matrix to adapt tools to the given machine.

## Objectives

1. Cluster data in order to attribute new data to the correct machine
2. Create a transformation matrix in order to normalize a machines data into a reference framework

## Running unit tests

Just run the python test file as you would any other file.

## Time stamps

Time stamps are in Microsoft filetime format!!

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
- axes positions -> seem to be oscillating -> fourier transform?
- axes velocities?
- spindle power: stSigPowerMotS
- commands:
  - stSigSpindleVelocity
  - stSigOperation

## Various notes

- does knowing the temperature allow us to make some kind of compensation on the data?
