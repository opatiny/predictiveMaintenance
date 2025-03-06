# Predictive maintenance project

## Context

Use warm-up data of micro5 milling machines in order to identify the current machine, and create a transformation matrix to adapt tools to the given machine.

## Objectives

1. Cluster data in order to attribute new data to the correct machine
2. Create a transformation matrix in order to normalize a machines data into a reference framework

## Signals that look interesting

- temperatures:
  - lrSigSpindleTemp
- axes currents
  - stSigAxCurrentB
  - stSigAxCurrentS
  - stSigAxCurrentX
  - stSigAxCurrentY
  - stSigAxCurrentZ
- error signals seems interesting as well
- axes positions -> 10 signals, seem to be oscillating -> fourier transform?
- axes velocities? -> 10 signals
- motors power: stSigPowerMotS
- consignes:
  - stSigSpindleVelocity
  - stSigOperation

## Various notes

- does knowing the temperature allow us to make some kind of compensation on the data?
