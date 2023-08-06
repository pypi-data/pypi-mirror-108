from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tones:
	"""Tones commands group definition. 54 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tones", core, parent)

	@property
	def voip(self):
		"""voip commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_voip'):
			from .Tones_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	@property
	def dcs(self):
		"""dcs commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcs'):
			from .Tones_.Dcs import Dcs
			self._dcs = Dcs(self._core, self._base)
		return self._dcs

	@property
	def audioInput(self):
		"""audioInput commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_audioInput'):
			from .Tones_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .Tones_.SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._base)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_spdifRight'):
			from .Tones_.SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._base)
		return self._spdifRight

	@property
	def demodulation(self):
		"""demodulation commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_demodulation'):
			from .Tones_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	def clone(self) -> 'Tones':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tones(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
