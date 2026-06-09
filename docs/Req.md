# Requirements

1. Read sensor value every 100 ms. Poll interval is configured via config.ini.

2. Sensor file name is configurable via config.ini.

3. Valid sensor values must be floating-point numbers in the range 0.0 to 100.0 (inclusive).

   Any value outside this range is considered a sensor failure.

4. Apply a configurable filter. Supported types: moving_average, moving_median, low_pass.

   Filter parameters (`window_size` or `alpha`) are configured via config.ini.

5. If filtered value > threshold, activate actuator. Threshold is configurable via config.ini.

6. The actuator will print a warning message but app will continue working.

7. If sensor fails (or file ends), output an error message and exit the app.

