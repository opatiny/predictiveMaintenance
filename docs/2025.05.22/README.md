# Summary of improvements of phase 3 (2025.05.22)

- Fix normalising function:
  - By default interpolate all data at a frequency of 2000Hz
  - Create a machine properties file which contains info on the specific machines, typically the unit used for current signal (amperes of milli-amperes). Convert all currents to amperes in the normalization function
- "Check" functions: Functions to detect issues with the data
- Alignment functions
- Function to plot sample frequency to verify frequency is correct
