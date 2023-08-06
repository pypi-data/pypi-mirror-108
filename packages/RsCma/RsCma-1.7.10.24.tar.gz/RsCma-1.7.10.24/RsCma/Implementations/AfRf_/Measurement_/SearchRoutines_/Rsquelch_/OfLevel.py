from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OfLevel:
	"""OfLevel commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ofLevel", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofLevel.fetch() \n
		Fetches the RF level at which the DUT opens the squelch so that the audio signal is not muted anymore. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_level: Range: -158 dBm to 16 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel?', suppressed)
		return Conversions.str_to_float(response)

	def calculate(self) -> float:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofLevel.calculate() \n
		Fetches the RF level at which the DUT opens the squelch so that the audio signal is not muted anymore. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_level: Range: -158 dBm to 16 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofLevel.read() \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_level: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFLevel?', suppressed)
		return Conversions.str_to_float(response)
