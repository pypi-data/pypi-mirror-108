from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 346 total commands, 15 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("measurement", core, parent)

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Measurement_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def delta(self):
		"""delta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delta'):
			from .Measurement_.Delta import Delta
			self._delta = Delta(self._core, self._base)
		return self._delta

	@property
	def voip(self):
		"""voip commands group. 7 Sub-classes, 4 commands."""
		if not hasattr(self, '_voip'):
			from .Measurement_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	@property
	def spdif(self):
		"""spdif commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_spdif'):
			from .Measurement_.Spdif import Spdif
			self._spdif = Spdif(self._core, self._base)
		return self._spdif

	@property
	def audioInput(self):
		"""audioInput commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .Measurement_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def demodulation(self):
		"""demodulation commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_demodulation'):
			from .Measurement_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def rfCarrier(self):
		"""rfCarrier commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfCarrier'):
			from .Measurement_.RfCarrier import RfCarrier
			self._rfCarrier = RfCarrier(self._core, self._base)
		return self._rfCarrier

	@property
	def searchRoutines(self):
		"""searchRoutines commands group. 8 Sub-classes, 5 commands."""
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

	@property
	def multiEval(self):
		"""multiEval commands group. 14 Sub-classes, 8 commands."""
		if not hasattr(self, '_multiEval'):
			from .Measurement_.MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._base)
		return self._multiEval

	@property
	def rfSettings(self):
		"""rfSettings commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Measurement_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def cdefinition(self):
		"""cdefinition commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_cdefinition'):
			from .Measurement_.Cdefinition import Cdefinition
			self._cdefinition = Cdefinition(self._core, self._base)
		return self._cdefinition

	@property
	def audioOutput(self):
		"""audioOutput commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioOutput'):
			from .Measurement_.AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._base)
		return self._audioOutput

	@property
	def sout(self):
		"""sout commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_sout'):
			from .Measurement_.Sout import Sout
			self._sout = Sout(self._core, self._base)
		return self._sout

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Measurement_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
