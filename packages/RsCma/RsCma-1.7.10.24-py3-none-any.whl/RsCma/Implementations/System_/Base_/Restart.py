from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restart:
	"""Restart commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restart", core, parent)

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Restart_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:RESTart \n
		Snippet: driver.system.base.restart.set() \n
		Restarts the test software. This action is faster than a restart of the instrument and often sufficient. \n
		"""
		self._core.io.write(f'SYSTem:BASE:RESTart')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:BASE:RESTart \n
		Snippet: driver.system.base.restart.set_with_opc() \n
		Restarts the test software. This action is faster than a restart of the instrument and often sufficient. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:BASE:RESTart')

	def clone(self) -> 'Restart':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Restart(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
