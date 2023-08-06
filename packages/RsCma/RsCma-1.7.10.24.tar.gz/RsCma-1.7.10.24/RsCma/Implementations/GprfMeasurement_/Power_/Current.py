from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.power.current.calculate() \n
		Queries the 'Power Current RMS' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_current_rms: 'Power Current RMS' result Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:POWer:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.power.current.fetch() \n
		Queries the 'Power Current RMS' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_current_rms: 'Power Current RMS' result Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:POWer:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.power.current.read() \n
		Queries the 'Power Current RMS' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_current_rms: 'Power Current RMS' result Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:POWer:CURRent?', suppressed)
		return response
