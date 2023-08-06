from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioOutput:
	"""AudioOutput commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: AudioOutput, default value after init: AudioOutput.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("audioOutput", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_audioOutput_get', 'repcap_audioOutput_set', repcap.AudioOutput.Nr1)

	def repcap_audioOutput_set(self, enum_value: repcap.AudioOutput) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AudioOutput.Default
		Default value after init: AudioOutput.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_audioOutput_get(self) -> repcap.AudioOutput:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ecircuitry(self):
		"""ecircuitry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecircuitry'):
			from .AudioOutput_.Ecircuitry import Ecircuitry
			self._ecircuitry = Ecircuitry(self._core, self._base)
		return self._ecircuitry

	@property
	def zbox(self):
		"""zbox commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_zbox'):
			from .AudioOutput_.Zbox import Zbox
			self._zbox = Zbox(self._core, self._base)
		return self._zbox

	@property
	def dimpedance(self):
		"""dimpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dimpedance'):
			from .AudioOutput_.Dimpedance import Dimpedance
			self._dimpedance = Dimpedance(self._core, self._base)
		return self._dimpedance

	@property
	def eimpedance(self):
		"""eimpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eimpedance'):
			from .AudioOutput_.Eimpedance import Eimpedance
			self._eimpedance = Eimpedance(self._core, self._base)
		return self._eimpedance

	@property
	def limpedance(self):
		"""limpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limpedance'):
			from .AudioOutput_.Limpedance import Limpedance
			self._limpedance = Limpedance(self._core, self._base)
		return self._limpedance

	def clone(self) -> 'AudioOutput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioOutput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
