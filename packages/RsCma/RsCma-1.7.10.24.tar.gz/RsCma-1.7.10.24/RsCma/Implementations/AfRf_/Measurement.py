from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 625 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("measurement", core, parent)

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Measurement_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def multiEval(self):
		"""multiEval commands group. 14 Sub-classes, 3 commands."""
		if not hasattr(self, '_multiEval'):
			from .Measurement_.MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._base)
		return self._multiEval

	@property
	def searchRoutines(self):
		"""searchRoutines commands group. 6 Sub-classes, 3 commands."""
		if not hasattr(self, '_searchRoutines'):
			from .Measurement_.SearchRoutines import SearchRoutines
			self._searchRoutines = SearchRoutines(self._core, self._base)
		return self._searchRoutines

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Measurement_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
