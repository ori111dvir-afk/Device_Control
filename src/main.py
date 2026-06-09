import time
import configparser

from sensor import Sensor
from filter import FILTER_MAP
from actuator import Actuator
from controller import Controller


def main() -> None:
    config = configparser.ConfigParser()
    config.read("config.ini")
    sensor = Sensor(config.get("sensor", "filename"))
    filter_class = FILTER_MAP[config.get("filter", "type")]
    if (config.get("filter","type") == "low_pass"):
        myfilter = filter_class(config.getfloat("filter","alpha"))
    else:
        myfilter = filter_class(config.getint("filter","window_size"))

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
    main()
