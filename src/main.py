"""Run the device control application.

This module is the entry point for the device control pipeline. It reads
configuration from a local INI file, creates the sensor, filter,
controller, and actuator objects, and then processes sensor values in a loop.
"""

import sys
import time
import configparser

from sensor import Sensor
from filter import FILTER_MAP
from actuator import Actuator
from controller import Controller


def main(config_path: str = "config.in") -> None:
    """Run the main device control loop.

    The function reads settings from the specified INI file, initializes all
    components, and then repeatedly polls the sensor at the configured interval
    (`main.poll_interval_ms`). Each raw sensor reading is filtered before being
    evaluated by the controller. When the controller threshold is exceeded, the
    actuator is activated.

    The loop terminates cleanly when the sensor reports failure or reaches end
    of file, and the sensor resource is always closed.

    Args:
        config_path: Path to the INI configuration file.

    Returns:
        None
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    sensor = Sensor(config.get("sensor", "filename"))
    filter_class = FILTER_MAP[config.get("filter", "type")]
    if config.get("filter", "type") == "low_pass":
        myfilter = filter_class(config.getfloat("filter", "alpha"))
    else:
        myfilter = filter_class(config.getint("filter", "window_size"))

    controller = Controller(config.getfloat("controller", "threshold"))
    actuator = Actuator()
    poll_interval_ms = config.getint("main", "poll_interval_ms")

    try:
        while True:
            time.sleep(poll_interval_ms / 1000)  # 100 ms

            raw = sensor.read_value()
            if raw is None:
                print("Error: sensor failure or end of data. Exiting.")
                break

            filtered = myfilter.apply(raw)
            print(f"Filtered value: {filtered:.2f}")
            if controller.check(filtered):
                actuator.activate(filtered)

    finally:
        sensor.close()


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.in"
    main(config_path)
