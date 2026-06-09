"""Filter classes for smoothing sensor values.

This module defines an abstract filter interface and concrete filter
implementations for moving average, moving median, and low-pass filtering.
"""

from abc import ABC, abstractmethod
from collections import deque
from statistics import median


class Filter(ABC):
    """Abstract base class for value filters."""

    @abstractmethod
    def apply(self, value: float) -> float:
        """Apply the filter to a new value.

        Args:
            value: The latest raw value from the sensor.

        Returns:
            The filtered value.
        """
        pass


class MovingAverageFilter(Filter):
    """Compute a sliding-window moving average."""

    def __init__(self, window_size: int = 5):
        """Initialize the moving average filter.

        Args:
            window_size: Number of most recent values included in the average.
        """
        self.values: deque[float] = deque(maxlen=window_size)

    def apply(self, value: float) -> float:
        """Update the window and return the current average."""
        self.values.append(value)
        return sum(self.values) / len(self.values)


class MovingMedianFilter(Filter):
    """Compute a sliding-window moving median."""

    def __init__(self, window_size: int = 5):
        """Initialize the moving median filter.

        Args:
            window_size: Number of most recent values included in the median.
        """
        self.values: deque[float] = deque(maxlen=window_size)

    def apply(self, value: float) -> float:
        """Update the window and return the current median."""
        self.values.append(value)
        return median(self.values)


class LowPassFilter(Filter):
    """Compute an exponential moving average low-pass filter."""

    def __init__(self, alpha: float = 1.0):
        """Initialize the low-pass filter.

        Args:
            alpha: Smoothing factor between 0.0 and 1.0.
        """
        self.alpha: float = alpha
        self.value: float = None

    def apply(self, value: float) -> float:
        """Apply the filter to the first value and initialize state."""
        self.value = value
        self.apply = self._apply_normal  # swap method after first call!
        return self.value

    def _apply_normal(self, value: float) -> float:
        """Apply the exponential moving average formula to subsequent values."""
        self.value = (self.alpha * value) + ((1 - self.alpha) * self.value)
        return self.value


FILTER_MAP = {
    "moving_average": MovingAverageFilter,
    "moving_median": MovingMedianFilter,
    "low_pass": LowPassFilter,
}