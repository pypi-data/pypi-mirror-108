from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lte:
	"""Lte commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lte", core, parent)

	@property
	def evm(self):
		"""evm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_evm'):
			from .Lte_.Evm import Evm
			self._evm = Evm(self._core, self._base)
		return self._evm

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Lte_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def modulation(self):
		"""modulation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Lte_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	def clone(self) -> 'Lte':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lte(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
