from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpdifRight:
	"""SpdifRight commands group definition. 12 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdifRight", core, parent)

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .SpdifRight_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .SpdifRight_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_deviation'):
			from .SpdifRight_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	@property
	def extreme(self):
		"""extreme commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_extreme'):
			from .SpdifRight_.Extreme import Extreme
			self._extreme = Extreme(self._core, self._base)
		return self._extreme

	def clone(self) -> 'SpdifRight':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpdifRight(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
