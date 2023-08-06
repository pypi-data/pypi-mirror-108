from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GprfMeasurement:
	"""GprfMeasurement commands group definition. 31 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gprfMeasurement", core, parent)

	@property
	def spectrum(self):
		"""spectrum commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_spectrum'):
			from .GprfMeasurement_.Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._base)
		return self._spectrum

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_power'):
			from .GprfMeasurement_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def fftSpecAn(self):
		"""fftSpecAn commands group. 1 Sub-classes, 8 commands."""
		if not hasattr(self, '_fftSpecAn'):
			from .GprfMeasurement_.FftSpecAn import FftSpecAn
			self._fftSpecAn = FftSpecAn(self._core, self._base)
		return self._fftSpecAn

	@property
	def iqRecorder(self):
		"""iqRecorder commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_iqRecorder'):
			from .GprfMeasurement_.IqRecorder import IqRecorder
			self._iqRecorder = IqRecorder(self._core, self._base)
		return self._iqRecorder

	def clone(self) -> 'GprfMeasurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GprfMeasurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
