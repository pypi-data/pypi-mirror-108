from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tetra:
	"""Tetra commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tetra", core, parent)

	@property
	def evm(self):
		"""evm commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_evm'):
			from .Tetra_.Evm import Evm
			self._evm = Evm(self._core, self._base)
		return self._evm

	@property
	def merror(self):
		"""merror commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_merror'):
			from .Tetra_.Merror import Merror
			self._merror = Merror(self._core, self._base)
		return self._merror

	def clone(self) -> 'Tetra':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tetra(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
