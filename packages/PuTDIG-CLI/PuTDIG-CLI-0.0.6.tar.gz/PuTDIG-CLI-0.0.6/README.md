# PuTDIG

Pumpkin Telemetry Discovery Injection and Generation program.

## Telemetry Benchmark Utility
`pumbench` can be used to measure the response time of each telemetry item on the bus.

First you must generate a bus definition using [pumqry](https://github.com/PumpkinSpace/PuTDIG-CLI): `pumqry -t kubos -p 1 -e -d -f bus.json`

Then you can run a benchmark: `pumbench -t i2c_driver -p /dev/ttyUSBX -f /path/to/save/to.json`
