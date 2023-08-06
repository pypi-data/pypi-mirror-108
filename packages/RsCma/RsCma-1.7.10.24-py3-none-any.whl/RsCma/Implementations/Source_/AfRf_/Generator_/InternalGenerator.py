from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InternalGenerator:
	"""InternalGenerator commands group definition. 20 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: InternalGen, default value after init: InternalGen.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("internalGenerator", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_internalGen_get', 'repcap_internalGen_set', repcap.InternalGen.Nr1)

	def repcap_internalGen_set(self, enum_value: repcap.InternalGen) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to InternalGen.Default
		Default value after init: InternalGen.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_internalGen_get(self) -> repcap.InternalGen:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .InternalGenerator_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .InternalGenerator_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .InternalGenerator_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def dtone(self):
		"""dtone commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtone'):
			from .InternalGenerator_.Dtone import Dtone
			self._dtone = Dtone(self._core, self._base)
		return self._dtone

	@property
	def multiTone(self):
		"""multiTone commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_multiTone'):
			from .InternalGenerator_.MultiTone import MultiTone
			self._multiTone = MultiTone(self._core, self._base)
		return self._multiTone

	@property
	def first(self):
		"""first commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_first'):
			from .InternalGenerator_.First import First
			self._first = First(self._core, self._base)
		return self._first

	@property
	def second(self):
		"""second commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_second'):
			from .InternalGenerator_.Second import Second
			self._second = Second(self._core, self._base)
		return self._second

	@property
	def third(self):
		"""third commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_third'):
			from .InternalGenerator_.Third import Third
			self._third = Third(self._core, self._base)
		return self._third

	@property
	def fourth(self):
		"""fourth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fourth'):
			from .InternalGenerator_.Fourth import Fourth
			self._fourth = Fourth(self._core, self._base)
		return self._fourth

	@property
	def dialing(self):
		"""dialing commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dialing'):
			from .InternalGenerator_.Dialing import Dialing
			self._dialing = Dialing(self._core, self._base)
		return self._dialing

	def clone(self) -> 'InternalGenerator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InternalGenerator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
