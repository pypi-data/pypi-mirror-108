from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioInput:
	"""AudioInput commands group definition. 30 total commands, 12 Sub-groups, 0 group commands
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
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .AudioInput_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .AudioInput_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def first(self):
		"""first commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_first'):
			from .AudioInput_.First import First
			self._first = First(self._core, self._base)
		return self._first

	@property
	def second(self):
		"""second commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_second'):
			from .AudioInput_.Second import Second
			self._second = Second(self._core, self._base)
		return self._second

	@property
	def counter(self):
		"""counter commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_counter'):
			from .AudioInput_.Counter import Counter
			self._counter = Counter(self._core, self._base)
		return self._counter

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .AudioInput_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def mlevel(self):
		"""mlevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlevel'):
			from .AudioInput_.Mlevel import Mlevel
			self._mlevel = Mlevel(self._core, self._base)
		return self._mlevel

	@property
	def aranging(self):
		"""aranging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aranging'):
			from .AudioInput_.Aranging import Aranging
			self._aranging = Aranging(self._core, self._base)
		return self._aranging

	@property
	def icoupling(self):
		"""icoupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icoupling'):
			from .AudioInput_.Icoupling import Icoupling
			self._icoupling = Icoupling(self._core, self._base)
		return self._icoupling

	@property
	def gcoupling(self):
		"""gcoupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gcoupling'):
			from .AudioInput_.Gcoupling import Gcoupling
			self._gcoupling = Gcoupling(self._core, self._base)
		return self._gcoupling

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .AudioInput_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def filterPy(self):
		"""filterPy commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .AudioInput_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	def clone(self) -> 'AudioInput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioInput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
