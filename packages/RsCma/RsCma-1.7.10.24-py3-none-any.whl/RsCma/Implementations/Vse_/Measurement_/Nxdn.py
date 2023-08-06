from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nxdn:
	"""Nxdn commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nxdn", core, parent)

	@property
	def symbols(self):
		"""symbols commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_symbols'):
			from .Nxdn_.Symbols import Symbols
			self._symbols = Symbols(self._core, self._base)
		return self._symbols

	def clone(self) -> 'Nxdn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nxdn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
