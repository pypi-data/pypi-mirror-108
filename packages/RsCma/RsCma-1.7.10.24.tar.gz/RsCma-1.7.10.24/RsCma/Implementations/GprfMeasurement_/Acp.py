from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acp:
	"""Acp commands group definition. 38 total commands, 4 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acp", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Acp_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def aclr(self):
		"""aclr commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_aclr'):
			from .Acp_.Aclr import Aclr
			self._aclr = Aclr(self._core, self._base)
		return self._aclr

	@property
	def power(self):
		"""power commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Acp_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def obw(self):
		"""obw commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_obw'):
			from .Acp_.Obw import Obw
			self._obw = Obw(self._core, self._base)
		return self._obw

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.initiate() \n
		Starts or continues the ACP measurement. \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:ACP')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.initiate_with_opc() \n
		Starts or continues the ACP measurement. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:ACP')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.stop() \n
		Pauses the ACP measurement. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:ACP')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.stop_with_opc() \n
		Pauses the ACP measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:ACP')

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.abort() \n
		Stops the ACP measurement. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:ACP')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:ACP \n
		Snippet: driver.gprfMeasurement.acp.abort_with_opc() \n
		Stops the ACP measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:ACP')

	def clone(self) -> 'Acp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Acp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
