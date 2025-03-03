class Utils:
    def normalizeTime(timeNs: list[float]) -> None:
        """
        Normalize epoch in ns to seconds from beginning of array.
        """
        startTime = timeNs[0]
        for i in range(len(timeNs)):
            timeNs[i] = (timeNs[i] - startTime) / 1e9
