from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DemodLeft:
	"""DemodLeft commands group definition. 12 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodLeft", core, parent)

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .DemodLeft_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .DemodLeft_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_deviation'):
			from .DemodLeft_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	@property
	def extreme(self):
		"""extreme commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_extreme'):
			from .DemodLeft_.Extreme import Extreme
			self._extreme = Extreme(self._core, self._base)
		return self._extreme

	def clone(self) -> 'DemodLeft':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DemodLeft(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
