from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Finish:
	"""Finish commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("finish", core, parent)

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Finish_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:FINish \n
		Snippet: driver.system.base.finish.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:BASE:FINish')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:BASE:FINish \n
		Snippet: driver.system.base.finish.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:BASE:FINish')

	def clone(self) -> 'Finish':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Finish(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
