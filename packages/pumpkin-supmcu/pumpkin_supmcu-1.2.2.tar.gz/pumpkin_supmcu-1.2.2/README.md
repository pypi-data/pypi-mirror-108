# pumpkin_supmcu Package

The `pumpkin_supmcu` package has the following functionality:

* Discover all telemetry items on a module, and put into telemetry definitions.
* Parse any telemetry item on a module given a module telemetry definition.
* Provide a universal I2C interface to integrate multiple I2C Masters.
* Request telemetry from any SupMCU module via I2C interface.
* Write commands to SupMCU modules via I2C interface.

The documentation for the `pumpkin_supmcu` package can be [found here](https://pumpkin-supmcu.readthedocs.io/en/latest/index.html).

### Telemetry Benchmark Utility
`utils/benchmark.py` can be used to measure the response time of each telemetry item on the bus.

First you must generate a bus definition using [pumqry](https://github.com/PumpkinSpace/PuTDIG-CLI): `pumqry -t kubos -p 1 -e -d -f bus.json` (example bus.json provided for reference).

Then you can run a benchmark: `python utils/benchmark.py -p /dev/ttyUSBX -f /path/to/save/to.json`
