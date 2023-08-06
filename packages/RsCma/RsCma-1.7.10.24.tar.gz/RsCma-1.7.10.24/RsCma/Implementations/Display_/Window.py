from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Window:
	"""Window commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Window, default value after init: Window.Win1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("window", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_window_get', 'repcap_window_set', repcap.Window.Win1)

	def repcap_window_set(self, enum_value: repcap.Window) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Window.Default
		Default value after init: Window.Win1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_window_get(self) -> repcap.Window:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Window_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	def clone(self) -> 'Window':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Window(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
