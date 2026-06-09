class Sensor:
    def __init__(self, filename: str = "sensor.dat"):
        self.filename = filename
        try:
            self.file = open(self.filename, "r")
        except OSError:
            print("Error: Cannot open sensor file.")
            self.file = None

    def read_value(self) -> float | None:
        """Read next sensor value, or return None on failure/EOF."""
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
        if self.file is not None:
            self.file.close()
            self.file = None