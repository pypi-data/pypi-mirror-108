from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 27 total commands, 8 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Power_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def elapsedStats(self):
		"""elapsedStats commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_elapsedStats'):
			from .Power_.ElapsedStats import ElapsedStats
			self._elapsedStats = ElapsedStats(self._core, self._base)
		return self._elapsedStats

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Power_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def minimum(self):
		"""minimum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_minimum'):
			from .Power_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def maximum(self):
		"""maximum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_maximum'):
			from .Power_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .Power_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def peak(self):
		"""peak commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_peak'):
			from .Power_.Peak import Peak
			self._peak = Peak(self._core, self._base)
		return self._peak

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_standardDev'):
			from .Power_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.initiate() \n
		Starts or continues the power measurement. \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:POWer')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.initiate_with_opc() \n
		Starts or continues the power measurement. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:POWer')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.stop() \n
		Pauses the power measurement. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:POWer')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.stop_with_opc() \n
		Pauses the power measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:POWer')

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.abort() \n
		Stops the power measurement. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:POWer')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.abort_with_opc() \n
		Stops the power measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:POWer')

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
