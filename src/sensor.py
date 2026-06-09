"""Sensor module for reading numeric values from a file.

This module provides a simple sensor abstraction that reads floating-point
values from a file line by line. Invalid data, out-of-range values, and end of
file are treated as sensor failures.
"""


class Sensor:
    """Read and validate sensor values from a text file.

    Attributes:
        filename: The path to the sensor data file.
        file: The open file object or None if the file could not be opened.
    """

    def __init__(self, filename: str = "sensor.dat"):
        """Open the sensor file for reading.

        Args:
            filename: Path to the file containing sensor values.
        """
        self.filename = filename
        try:
            self.file = open(self.filename, "r")
        except OSError:
            print("Error: Cannot open sensor file.")
            self.file = None

    def read_value(self) -> float | None:
        """Read the next valid sensor value.

        Reads one line from the sensor file, converts it to a float, and validates
        that it is within the range 0.0 to 100.0 inclusive.

        Returns:
            The float value if valid, or None for invalid data, out-of-range
            values, file errors, or end of file.
        """
        if self.file is None:
            return None

        line = self.file.readline()
        if not line:
            return None  # EOF → sensor failure

        try:
            value = float(line.strip())
        except ValueError:
            return None  # not a valid float → sensor failure

        # Enforce 0.0–100.0 inclusive
        if value < 0.0 or value > 100.0:
            return None  # out-of-range → sensor failure

        return value

    def close(self) -> None:
        """Close the sensor file if it is open."""
        if self.file is not None:
            self.file.close()
            self.file = None