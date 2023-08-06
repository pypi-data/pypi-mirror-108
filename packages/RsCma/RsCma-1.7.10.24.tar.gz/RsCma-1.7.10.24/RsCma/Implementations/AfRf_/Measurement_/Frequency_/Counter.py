from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Counter:
	"""Counter commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("counter", core, parent)

	@property
	def freqError(self):
		"""freqError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_freqError'):
			from .Counter_.FreqError import FreqError
			self._freqError = FreqError(self._core, self._base)
		return self._freqError

	def initiate(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:FREQuency:COUNter \n
		Snippet: driver.afRf.measurement.frequency.counter.initiate() \n
		Starts the search procedure to find an RF signal. \n
		"""
		self._core.io.write(f'INITiate:AFRF:MEASurement<Instance>:FREQuency:COUNter')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:FREQuency:COUNter \n
		Snippet: driver.afRf.measurement.frequency.counter.initiate_with_opc() \n
		Starts the search procedure to find an RF signal. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:FREQuency:COUNter')

	def abort(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:FREQuency:COUNter \n
		Snippet: driver.afRf.measurement.frequency.counter.abort() \n
		Aborts the search procedure for an RF signal. The configured RF settings are not modified. \n
		"""
		self._core.io.write(f'ABORt:AFRF:MEASurement<Instance>:FREQuency:COUNter')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:FREQuency:COUNter \n
		Snippet: driver.afRf.measurement.frequency.counter.abort_with_opc() \n
		Aborts the search procedure for an RF signal. The configured RF settings are not modified. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:FREQuency:COUNter')

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Frequency: float: Frequency of signal peak Range: 0 Hz to 3 GHz, Unit: Hz
			- Level: float: Power of signal peak Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_float('Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Frequency: float = None
			self.Level: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:FREQuency:COUNter \n
		Snippet: value: FetchStruct = driver.afRf.measurement.frequency.counter.fetch() \n
		Queries the search procedure results. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:FREQuency:COUNter?', self.__class__.FetchStruct())

	def clone(self) -> 'Counter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Counter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
