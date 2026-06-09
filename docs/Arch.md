\# Architecture Overview



\## Project Context

\- Pet project for learning Python coming from a C/C++ background

\- Goals:

&#x20; - Refresh programming skills in Python

&#x20; - Learn AI-assisted development

\- Intentionally kept simple — complexity added only when it teaches something

\- Preferred style: explain concepts by comparison to C/C++ equivalents



\## Components



\### Sensor

\- Class: `Sensor`

\- Reads floating-point values from a file, line by line

\- Validates range 0.0–100.0

\- Returns `None` on failure or EOF



\### Filter

\- Abstract base class: `Filter` (ABC)

\- Concrete implementations:

&#x20; - `MovingAverageFilter(Filter)` — sliding window average

&#x20; - `MovingMedianFilter(Filter)` — sliding window median

&#x20; - `LowPassFilter(Filter)` — exponential moving average (EMA)

\- All filters expose a single interface: `apply(value: float) -> float`

\- Selected and instantiated via `FILTER\_MAP` factory dictionary



\### Controller

\- Class: `Controller`

\- Compares filtered value against configurable threshold

\- Returns `True` if value exceeds threshold



\### Actuator

\- Class: `Actuator`

\- Prints warning message when activated

\- App continues after activation



\## Data Flow

Sensor → Filter → Controller → Actuator



\## Configuration (config.ini)

\- `\[sensor]` — filename, poll\_interval\_ms

\- `\[filter]` — type, window\_size, alpha

\- `\[controller]` — threshold



\## Constraints

\- Safe fallback on sensor failure — error message and clean exit

\- All parameters configurable via config.ini, no hardcoded values

