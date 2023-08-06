from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 9 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Data_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def fsk(self):
		"""fsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsk'):
			from .Data_.Fsk import Fsk
			self._fsk = Fsk(self._core, self._base)
		return self._fsk

	def initiate(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.initiate() \n
		Starts or continues the measurement. \n
		"""
		self._core.io.write(f'INITiate:AFRF:MEASurement<Instance>:DATA')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.initiate_with_opc() \n
		Starts or continues the measurement. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:DATA')

	def stop(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.stop() \n
		Pauses the measurement. \n
		"""
		self._core.io.write(f'STOP:AFRF:MEASurement<Instance>:DATA')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.stop_with_opc() \n
		Pauses the measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:AFRF:MEASurement<Instance>:DATA')

	def abort(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.abort() \n
		Stops the measurement. \n
		"""
		self._core.io.write(f'ABORt:AFRF:MEASurement<Instance>:DATA')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:DATA \n
		Snippet: driver.afRf.measurement.data.abort_with_opc() \n
		Stops the measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:DATA')

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
