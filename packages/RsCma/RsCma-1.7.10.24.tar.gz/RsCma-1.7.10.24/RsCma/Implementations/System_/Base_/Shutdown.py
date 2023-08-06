from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shutdown:
	"""Shutdown commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shutdown", core, parent)

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Shutdown_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:SHUTdown \n
		Snippet: driver.system.base.shutdown.set() \n
		Shuts down the test software and shows the desktop of the operating system. \n
		"""
		self._core.io.write(f'SYSTem:BASE:SHUTdown')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:BASE:SHUTdown \n
		Snippet: driver.system.base.shutdown.set_with_opc() \n
		Shuts down the test software and shows the desktop of the operating system. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:BASE:SHUTdown')

	def clone(self) -> 'Shutdown':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Shutdown(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
