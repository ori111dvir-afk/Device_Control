"""Controller module for threshold evaluation.

The controller determines whether a filtered sensor value exceeds a configured
threshold.
"""


class Controller:
    """Check filtered values against a threshold."""

    def __init__(self, threshold: float = 50.0):
        """Initialize the controller.

        Args:
            threshold: Value above which the actuator should activate.
        """
        self.threshold = threshold

    def check(self, value: float) -> bool:
        """Return True if the value exceeds the threshold.

        Args:
            value: The filtered sensor value.

        Returns:
            True if the value is greater than the configured threshold.
        """
        return value > self.threshold
