from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bits:
	"""Bits commands group definition. 4 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bits", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Bits_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Bits_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def next(self):
		"""next commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_next'):
			from .Bits_.Next import Next
			self._next = Next(self._core, self._base)
		return self._next

	def clear(self, filter_py: str = None, mode: enums.ExpressionMode = None) -> None:
		"""SCPI: STATus:EVENt:BITS:CLEar \n
		Snippet: driver.status.event.bits.clear(filter_py = '1', mode = enums.ExpressionMode.REGex) \n
		No command help available \n
			:param filter_py: No help available
			:param mode: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_py', filter_py, DataType.String, True), ArgSingle('mode', mode, DataType.Enum, True))
		self._core.io.write(f'STATus:EVENt:BITS:CLEar {param}'.rstrip())

	def clone(self) -> 'Bits':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bits(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
