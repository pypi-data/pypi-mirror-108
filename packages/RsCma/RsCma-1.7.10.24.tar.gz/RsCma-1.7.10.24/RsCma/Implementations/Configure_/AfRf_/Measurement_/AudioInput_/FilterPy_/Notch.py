from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Notch:
	"""Notch commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: Notch, default value after init: Notch.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("notch", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_notch_get', 'repcap_notch_set', repcap.Notch.Nr1)

	def repcap_notch_set(self, enum_value: repcap.Notch) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Notch.Default
		Default value after init: Notch.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_notch_get(self) -> repcap.Notch:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Notch_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Notch_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	def clone(self) -> 'Notch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Notch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
