from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 24 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voip", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Voip_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Voip_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def afSignal(self):
		"""afSignal commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_afSignal'):
			from .Voip_.AfSignal import AfSignal
			self._afSignal = AfSignal(self._core, self._base)
		return self._afSignal

	def clone(self) -> 'Voip':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Voip(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
