from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


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
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .AudioOutput_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .AudioOutput_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .AudioOutput_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def first(self):
		"""first commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_first'):
			from .AudioOutput_.First import First
			self._first = First(self._core, self._base)
		return self._first

	@property
	def second(self):
		"""second commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_second'):
			from .AudioOutput_.Second import Second
			self._second = Second(self._core, self._base)
		return self._second

	def clone(self) -> 'AudioOutput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioOutput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
