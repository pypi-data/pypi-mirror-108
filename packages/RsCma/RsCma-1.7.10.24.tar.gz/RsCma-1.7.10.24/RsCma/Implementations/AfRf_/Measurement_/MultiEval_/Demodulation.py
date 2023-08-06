from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 76 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodulation", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Demodulation_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def modDepth(self):
		"""modDepth commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .Demodulation_.ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._base)
		return self._modDepth

	@property
	def fdeviation(self):
		"""fdeviation commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Demodulation_.Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._base)
		return self._fdeviation

	@property
	def fmStereo(self):
		"""fmStereo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fmStereo'):
			from .Demodulation_.FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._base)
		return self._fmStereo

	@property
	def pdeviation(self):
		"""pdeviation commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Demodulation_.Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._base)
		return self._pdeviation

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
