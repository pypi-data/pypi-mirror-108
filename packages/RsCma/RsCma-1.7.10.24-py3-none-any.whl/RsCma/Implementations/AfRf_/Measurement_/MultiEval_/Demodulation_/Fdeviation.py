from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdeviation:
	"""Fdeviation commands group definition. 28 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdeviation", core, parent)

	@property
	def rms(self):
		"""rms commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rms'):
			from .Fdeviation_.Rms import Rms
			self._rms = Rms(self._core, self._base)
		return self._rms

	@property
	def peak(self):
		"""peak commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_peak'):
			from .Fdeviation_.Peak import Peak
			self._peak = Peak(self._core, self._base)
		return self._peak

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Fdeviation_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .Fdeviation_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .Fdeviation_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_deviation'):
			from .Fdeviation_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	def clone(self) -> 'Fdeviation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fdeviation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
