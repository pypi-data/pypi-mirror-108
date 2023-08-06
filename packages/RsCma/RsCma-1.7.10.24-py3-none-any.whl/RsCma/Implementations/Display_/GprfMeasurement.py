from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GprfMeasurement:
	"""GprfMeasurement commands group definition. 5 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gprfMeasurement", core, parent)

	@property
	def extPwrSensor(self):
		"""extPwrSensor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_extPwrSensor'):
			from .GprfMeasurement_.ExtPwrSensor import ExtPwrSensor
			self._extPwrSensor = ExtPwrSensor(self._core, self._base)
		return self._extPwrSensor

	@property
	def spectrum(self):
		"""spectrum commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_spectrum'):
			from .GprfMeasurement_.Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._base)
		return self._spectrum

	@property
	def fftSpecAn(self):
		"""fftSpecAn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fftSpecAn'):
			from .GprfMeasurement_.FftSpecAn import FftSpecAn
			self._fftSpecAn = FftSpecAn(self._core, self._base)
		return self._fftSpecAn

	@property
	def acp(self):
		"""acp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_acp'):
			from .GprfMeasurement_.Acp import Acp
			self._acp = Acp(self._core, self._base)
		return self._acp

	def clone(self) -> 'GprfMeasurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GprfMeasurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
