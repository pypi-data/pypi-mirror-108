from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ...Internal.Types import DataType
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqRecorder:
	"""IqRecorder commands group definition. 13 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqRecorder", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .IqRecorder_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def talignment(self):
		"""talignment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_talignment'):
			from .IqRecorder_.Talignment import Talignment
			self._talignment = Talignment(self._core, self._base)
		return self._talignment

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .IqRecorder_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def bin(self):
		"""bin commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bin'):
			from .IqRecorder_.Bin import Bin
			self._bin = Bin(self._core, self._base)
		return self._bin

	@property
	def reliability(self):
		"""reliability commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reliability'):
			from .IqRecorder_.Reliability import Reliability
			self._reliability = Reliability(self._core, self._base)
		return self._reliability

	def initiate(self, save_to_iq_file: enums.FileSave = None) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: driver.gprfMeasurement.iqRecorder.initiate(save_to_iq_file = enums.FileSave.OFF) \n
		Starts or continues the I/Q recorder measurement. \n
			:param save_to_iq_file: OFF | ON | ONLY Optional parameter, selecting whether the results are written to an I/Q file, to the memory or both. For selection of the I/Q file, see method RsCma.Configure.GprfMeasurement.IqRecorder.iqFile. OFF The results are only stored in the memory. ON The results are stored in the memory and in the file. ONLY The results are only stored in the file.
		"""
		param = ''
		if save_to_iq_file:
			param = Conversions.enum_scalar_to_str(save_to_iq_file, enums.FileSave)
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:IQRecorder {param}'.strip())

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: driver.gprfMeasurement.iqRecorder.abort() \n
		Stops the I/Q recorder measurement. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:IQRecorder')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: driver.gprfMeasurement.iqRecorder.abort_with_opc() \n
		Stops the I/Q recorder measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:IQRecorder')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: driver.gprfMeasurement.iqRecorder.stop() \n
		Pauses the I/Q recorder measurement. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:IQRecorder')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: driver.gprfMeasurement.iqRecorder.stop_with_opc() \n
		Pauses the I/Q recorder measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:IQRecorder')

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: value: List[float] = driver.gprfMeasurement.iqRecorder.read() \n
		Returns the I and Q amplitudes in the format specified by method RsCma.FormatPy.Base.data. For a detailed description of
		the data formats, see 'ASCII and Binary Data Formats'. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: iq_samples: For ASCII format: I/Q amplitudes in alternating order (I_1,Q_1, ...,I_n,Q_n) , as voltages. For REAL format: Binary block data consisting of the parts listed in the table below. There are no commas within this parameter."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:IQRecorder?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:IQRecorder \n
		Snippet: value: List[float] = driver.gprfMeasurement.iqRecorder.fetch() \n
		Returns the I and Q amplitudes in the format specified by method RsCma.FormatPy.Base.data. For a detailed description of
		the data formats, see 'ASCII and Binary Data Formats'. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: iq_samples: For ASCII format: I/Q amplitudes in alternating order (I_1,Q_1, ...,I_n,Q_n) , as voltages. For REAL format: Binary block data consisting of the parts listed in the table below. There are no commas within this parameter."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:IQRecorder?', suppressed)
		return response

	def clone(self) -> 'IqRecorder':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqRecorder(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
