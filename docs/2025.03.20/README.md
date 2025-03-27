# Project intermediate results (2025.03.20)

## Sorting data points by time

The original data points are not sorted by timestamp, and also have duplicate timestamps.

![./data-not-sorted.png](./data-not-sorted.png)

After sorting:
![./sort-by-time.png](./sort-by-time.png)

## Plot axis B current from different samples

We see that:

- the various signals are not perfectly aligned
- We have a lot of variation for one single machine -> currents are influenced by the temperature!!

![./axisB-currents-mecatis.png](./axisB-currents-mecatis.png)
![./axisB-currents-mecatis-zoom.png](./axisB-currents-mecatis-zoom.png)

## Spindle currents

On the orange signal: weird vibrations appear on the signal -> do a Fourier transform to determine what these frequencies could be.

![./spindle-currents-mecatis.png](./spindle-currents-mecatis.png)
![./spindle-currents-mecatis-zoom.png](./spindle-currents-mecatis-zoom.png)
![./spindle-currents-mecatis-zoom2.png](./spindle-currents-mecatis-zoom2.png)
