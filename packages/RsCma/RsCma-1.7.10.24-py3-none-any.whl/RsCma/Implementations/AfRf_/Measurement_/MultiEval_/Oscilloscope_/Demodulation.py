from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 8 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodulation", core, parent)

	@property
	def pdeviation(self):
		"""pdeviation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Demodulation_.Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._base)
		return self._pdeviation

	@property
	def modDepth(self):
		"""modDepth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .Demodulation_.ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._base)
		return self._modDepth

	@property
	def lsbLevel(self):
		"""lsbLevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lsbLevel'):
			from .Demodulation_.LsbLevel import LsbLevel
			self._lsbLevel = LsbLevel(self._core, self._base)
		return self._lsbLevel

	@property
	def usbLevel(self):
		"""usbLevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbLevel'):
			from .Demodulation_.UsbLevel import UsbLevel
			self._usbLevel = UsbLevel(self._core, self._base)
		return self._usbLevel

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
