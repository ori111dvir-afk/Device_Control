# filter.py
from abc import ABC, abstractmethod
from collections import deque
from statistics import median



class Filter(ABC):
    @abstractmethod
    def apply(self, value: float) -> float:
        pass

class MovingAverageFilter(Filter):
    def __init__(self, window_size: int = 5):
        self.values: deque[float] = deque(maxlen=window_size)

    def apply(self, value: float) -> float:
        self.values.append(value)
        return sum(self.values) / len(self.values)

class MovingMedianFilter(Filter):
    def __init__(self, window_size: int = 5):
        self.values: deque[float] = deque(maxlen=window_size)

    def apply(self, value: float) -> float:
        self.values.append(value)
        return median(self.values)

class LowPassFilter(Filter):
    def __init__(self, alpha: float = 1.0):
        self.alpha: float = alpha
        self.value: float = None

# output = alpha × new_value + (1 - alpha) × previous_output
    def apply(self, value: float) -> float:
        self.value = value
        self.apply = self._apply_normal  # swap method after first call!
        return self.value
    
    def _apply_normal(self, value: float) -> float:
        self.value = (self.alpha*value) + ((1-self.alpha) * self.value)
        return self.value


FILTER_MAP = {
    "moving_average": MovingAverageFilter,
    "moving_median":  MovingMedianFilter,
    "low_pass":       LowPassFilter,
}