"""Actuator module for responding to threshold violations.

The actuator currently uses a simple console warning to indicate that the
filtered value exceeded the configured threshold.
"""


class Actuator:
    """Execute an actuator response when a threshold is exceeded."""

    def activate(self, value: float) -> None:
        """Activate the actuator response.

        Args:
            value: The filtered value that triggered activation.
        """
        print(f"WARNING: filtered value {value:.2f} exceeded threshold!")
