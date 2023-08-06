# ##############################################################################
#  Copyright (c) 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This File may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY  OF DESIGN, MERCHANTABILITY AND                      #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""Logs the required time to prepare telemetry per module by querying each telemetry item and recording how long it
takes to get a ready response from the SupMCU module.."""

import sys
import logging
from pathlib import Path
from typing import List, Iterable, Dict, Tuple
from dataclasses import dataclass, field

from plumbum import cli

from pumpkin_supmcu.supmcu.discovery import get_values

# Try and import all of the various I2CMaster implementations.
try:
    from pumpkin_supmcu.i2cdriver import I2CDriverMaster
except ImportError:
    I2CDriverMaster = None
try:
    from pumpkin_supmcu.linux import I2CLinuxMaster
except ImportError:
    I2CLinuxMaster = None
try:
    from pumpkin_supmcu.aardvark import I2CAardvarkMaster
except ImportError:
    I2CAardvarkMaster = None
try:
    from pumpkin_supmcu.kubos import I2CKubosMaster
except ImportError:
    I2CKubosMaster = None

from pumpkin_supmcu.supmcu.types import TelemetryType, SupMCUModuleDefinition, SupMCUTelemetryDefinition
from putdig.common import import_bus_telemetry_definition, export_dataclass
from putdig.common.types import ModuleDefinition

logger = logging.getLogger('telemetry-benchmark')
logger.setLevel(logging.INFO)
stdout = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(stdout)


@dataclass
class ModuleResults:
    name: str
    total: float = 0
    average: float = 0
    fails: List[Tuple[str, int]] = field(default_factory=list)
    supmcu_telemetry: Dict[str, float] = field(default_factory=dict)
    module_telemetry: Dict[str, float] = field(default_factory=dict)


class BenchmarkResults:
    """
    Records the results of the telemetry benchmark.
    Records dictionary results of the form:
        {
            MODULE: {
                'total': float,         # total response time of all telem in seconds
                'fails': [(str, int)]   # list of telem names, index that failed
                TelemetryType.SupMCU: {
                    TELEM_NAME: float,  # response time for this telemetry
                    ...
                }
                TelemetryType.Module: {
                    TELEM_NAME: float,  # response time for this telemetry
                    ...
                }
            }
        }
    """

    def __init__(self):
        self.results_dict = {}

    def __str__(self):
        string = '\n'
        string += '=== Benchmark Results ===\n\n'
        for module in self.results_dict:
            string += '---' + module + '---\n'
            string += f'total response time: {self.results_dict[module].total}\n'
            string += f'avg response time: {self.results_dict[module].average}\n'
            string += f'failed items: {len(self.results_dict[module].fails)}\n'
        return string

    def record(self, module_name: str, telem: SupMCUTelemetryDefinition, telem_type: TelemetryType, response_time: float):
        """
        Records the response time of a telemetry item.
        """
        if module_name not in self.results_dict:
            self.results_dict[module_name] = ModuleResults(module_name)
        if response_time == 0:
            self.results_dict[module_name].fails.append((telem.name, telem.idx))
            return

        module_results = self.results_dict.get(module_name)
        if telem_type == TelemetryType.SupMCU:
            module_results.supmcu_telemetry[telem.name] = response_time
        else:
            module_results.module_telemetry[telem.name] = response_time

        module_results.total += response_time

    def num_telem(self, module: str):
        return len(self.results_dict[module].supmcu_telemetry) + \
               len(self.results_dict[module].module_telemetry)

    def process(self):
        for module in self.results_dict:
            self.results_dict[module].average = self.results_dict[module].total / self.num_telem(module)

    def save(self, path: Path):
        logger.info(f'Saving results to {path}\n')
        export_dataclass(list(self.results_dict.values()), path)


class Benchmark:
    """
    Benchmarks telemetry response time of a bus.
    """

    DELAY_INCREMENT_SEC: float = 0.001  # each time telem isn't ready yet, increase the delay and re-request
    DELAY_MAX_SEC: float = 0.050        # once the delay is greater than this, give up
    
    def __init__(self, i2c_master: I2CDriverMaster, bus_definition: List[ModuleDefinition]):
        self.i2c_master = i2c_master
        self.bus_definition = bus_definition
        self._delay_increment = Benchmark.DELAY_INCREMENT_SEC
        self._delay_max = Benchmark.DELAY_MAX_SEC
        self._results = BenchmarkResults()

    def measure_bus_telemetry(self, mods: List):
        if mods:
            modules = (mod.definition for mod in self.bus_definition if mod.definition.name in mods)
        else:
            modules = (mod.definition for mod in self.bus_definition)
        for module in modules:
            self.measure_module_telem(module, list(module.supmcu_telemetry.values()), TelemetryType.SupMCU)
            self.measure_module_telem(module, list(module.module_telemetry.values()), TelemetryType.Module)
        self.results.process()

    def measure_module_telem(self, module: SupMCUModuleDefinition, telem: List[SupMCUTelemetryDefinition],
                             telem_type: TelemetryType):
        for t in telem:
            read_seconds = self.measure_telem_read(module, t, telem_type)
            if read_seconds != 0:
                logger.info(f'{module.name} {t.name} ready in {read_seconds * 1000} ms')
            else:
                logger.info(f'{module.name} {t.name} failed')
            self.results.record(module.name, t, telem_type, read_seconds)

    def measure_telem_read(self, module: SupMCUModuleDefinition, telem: SupMCUTelemetryDefinition,
                           telem_type: TelemetryType) -> float:
        logger.debug(f'measuring {module.name} {telem.name}')
        if telem_type == TelemetryType.SupMCU:
            cmd_name = 'SUP'
        else:
            cmd_name = module.cmd_name
        for i in self.delays():
            try:
                get_values(self.i2c_master, module.address, cmd_name, telem.idx, telem.format, response_delay=i)
                return i
            except ValueError as e:
                logger.debug(e)
                pass
            if i >= self.delay_max:
                return 0    # couldn't read telem under max delay

    @property
    def results(self) -> BenchmarkResults:
        return self._results

    def delays(self) -> Iterable[float]:
        i = 1
        while True:
            yield float(i) * self._delay_increment
            i += 1

    @property
    def delay_increment(self):
        return self._delay_increment

    @delay_increment.setter
    def delay_increment(self, value: float):
        if value <= 0:
            raise ValueError(f'value cannot be less than or equal to 0: {value}')
        self._delay_increment = value

    @property
    def delay_max(self):
        return self._delay_max

    @delay_max.setter
    def delay_max(self, value: float):
        if value <= 0:
            raise ValueError(f'value cannot be less than or equal to 0: {value}')
        self._delay_max = value


class BenchmarkApp(cli.Application):
    """
    CLI app for running supmcu telem benchmark
    """

    port = cli.SwitchAttr(
        ["-p", "--port"],
        str,
        mandatory=True,
        help="COM# (Windows), device path (Linux, type i2cdriver), or bus # (Linux/Kubos, type linux/kubos) to I2C "
             "Master device "
    )

    i2c_type = cli.SwitchAttr(
        ["-t", "--type"],
        str,
        mandatory=True,
        help="Type of I2C device at -p. Can be i2cdriver, aardvark, linux, kubos, all other values rejected"
    )

    bus_json = cli.SwitchAttr(
        ["-b", "--bus-json"],
        str,
        mandatory=True,
        help="The bus definition json to use for the benchmark."
    )

    file = cli.SwitchAttr(
        ["-f", "--file"],
        str,
        default=None,
        help="The file to save JSON results to"
    )

    def main(self, *modules: str):
        modules = (mod.upper() for mod in modules)
        bus: List[ModuleDefinition] = import_bus_telemetry_definition(Path(self.bus_json))
        self.i2c_type = self.i2c_type.lower()
        if self.i2c_type == "i2cdriver":
            if I2CDriverMaster is None:
                raise NotImplementedError("I2CDriverMaster is not implemented for this system")
            i2c_master = I2CDriverMaster(self.port)
        elif self.i2c_type == "aardvark":
            if I2CAardvarkMaster is None:
                raise NotImplementedError("I2CAardvarkMaster is not implemented for this system")
            i2c_master = I2CAardvarkMaster(self.port)
        elif self.i2c_type == "linux":
            if I2CLinuxMaster is None:
                raise NotImplementedError("I2CLinuxMaster is not implemented for this system")
            i2c_master = I2CLinuxMaster(int(self.port))
        elif self.i2c_type == "kubos":
            if I2CKubosMaster is None:
                raise NotImplementedError("I2CKubosMaster is not implemented for this system")
            i2c_master = I2CKubosMaster(int(self.port))
        else:
            raise ValueError("Type must be 'i2cdriver, 'aardvark', or 'linux'")

        benchmark = Benchmark(i2c_master, bus)
        benchmark.measure_bus_telemetry(list(modules))
        logger.info(benchmark.results)

        if self.file is not None:
            benchmark.results.save(Path(self.file))


def execute():
    BenchmarkApp.run()


if __name__ == "__main__":
    execute()
