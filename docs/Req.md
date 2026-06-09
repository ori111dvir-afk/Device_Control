\# Requirements

1\. Read sensor value every 100 ms. Configured via config.ini.

2\. Valid sensor values must be floating-point numbers in the range 0.0 to 100.0 (inclusive).

&#x20;  Any value outside this range is considered a sensor failure.

3\. Apply a configurable filter. Supported types: moving\_average, moving\_median, low\_pass.

&#x20;  Filter parameters are configured via config.ini.

4\. If filtered value > threshold, activate actuator. Threshold is configurable via config.ini.

5\. The actuator will print a warning message but app will continue working.

6\. If sensor fails (or file ends), output an error message and exit the app.

