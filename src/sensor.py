"""Sensor module for reading numeric values from a file.

This module provides a simple sensor abstraction that reads floating-point
values from a file line by line. It returns a `SensorResult` dataclass which
contains the numeric value (or None) and a status string.
"""

from dataclasses import dataclass


@dataclass
class SensorResult:
    value: float | None
    status: str


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
            print("Sensor file not found, please check the file path, exiting.")
            self.file = None

    def read_value(self) -> SensorResult:
        """Read the next sensor value and return a SensorResult.

        Status values:
          - "ok": valid float within 0.0–100.0
          - "invalid-value": file errors, EOF, or non-numeric data
          - "out-of-range": numeric but outside allowed range
        """
        if self.file is None:
            return SensorResult(None, "invalid-value")

        line = self.file.readline()
        if not line:
            return SensorResult(None, "invalid-value")  # EOF → sensor failure

        try:
            value = float(line.strip())
        except ValueError:
            return SensorResult(None, "invalid-value")  # not a valid float → sensor failure

        # Enforce 0.0–100.0 inclusive
        if value < 0.0 or value > 100.0:
            return SensorResult(None, "out-of-range")

        return SensorResult(value, "ok")

    def close(self) -> None:
        """Close the sensor file if it is open."""
        if self.file is not None:
            self.file.close()
            self.file = None