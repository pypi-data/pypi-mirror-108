from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioInput:
	"""AudioInput commands group definition. 6 total commands, 6 Sub-groups, 0 group commands
	Repeated Capability: AudioInput, default value after init: AudioInput.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("audioInput", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_audioInput_get', 'repcap_audioInput_set', repcap.AudioInput.Nr1)

	def repcap_audioInput_set(self, enum_value: repcap.AudioInput) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AudioInput.Default
		Default value after init: AudioInput.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_audioInput_get(self) -> repcap.AudioInput:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def thDistortion(self):
		"""thDistortion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thDistortion'):
			from .AudioInput_.ThDistortion import ThDistortion
			self._thDistortion = ThDistortion(self._core, self._base)
		return self._thDistortion

	@property
	def thdNoise(self):
		"""thdNoise commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thdNoise'):
			from .AudioInput_.ThdNoise import ThdNoise
			self._thdNoise = ThdNoise(self._core, self._base)
		return self._thdNoise

	@property
	def snRatio(self):
		"""snRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snRatio'):
			from .AudioInput_.SnRatio import SnRatio
			self._snRatio = SnRatio(self._core, self._base)
		return self._snRatio

	@property
	def sinad(self):
		"""sinad commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinad'):
			from .AudioInput_.Sinad import Sinad
			self._sinad = Sinad(self._core, self._base)
		return self._sinad

	@property
	def snnRatio(self):
		"""snnRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snnRatio'):
			from .AudioInput_.SnnRatio import SnnRatio
			self._snnRatio = SnnRatio(self._core, self._base)
		return self._snnRatio

	@property
	def sndRatio(self):
		"""sndRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sndRatio'):
			from .AudioInput_.SndRatio import SndRatio
			self._sndRatio = SndRatio(self._core, self._base)
		return self._sndRatio

	def clone(self) -> 'AudioInput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioInput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
