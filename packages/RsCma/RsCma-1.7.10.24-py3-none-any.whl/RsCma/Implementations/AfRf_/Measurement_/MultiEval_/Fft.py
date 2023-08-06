from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fft:
	"""Fft commands group definition. 92 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fft", core, parent)

	@property
	def demodulation(self):
		"""demodulation commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodulation'):
			from .Fft_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def audioInput(self):
		"""audioInput commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .Fft_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdif(self):
		"""spdif commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdif'):
			from .Fft_.Spdif import Spdif
			self._spdif = Spdif(self._core, self._base)
		return self._spdif

	@property
	def voip(self):
		"""voip commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_voip'):
			from .Fft_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	@property
	def spdifRight(self):
		"""spdifRight commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifRight'):
			from .Fft_.SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._base)
		return self._spdifRight

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .Fft_.SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._base)
		return self._spdifLeft

	@property
	def demodLeft(self):
		"""demodLeft commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodLeft'):
			from .Fft_.DemodLeft import DemodLeft
			self._demodLeft = DemodLeft(self._core, self._base)
		return self._demodLeft

	@property
	def demodRight(self):
		"""demodRight commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodRight'):
			from .Fft_.DemodRight import DemodRight
			self._demodRight = DemodRight(self._core, self._base)
		return self._demodRight

	def clone(self) -> 'Fft':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fft(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
