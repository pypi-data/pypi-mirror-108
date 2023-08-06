from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 35 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodulation", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Demodulation_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def pdeviation(self):
		"""pdeviation commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Demodulation_.Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._base)
		return self._pdeviation

	@property
	def modDepth(self):
		"""modDepth commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .Demodulation_.ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._base)
		return self._modDepth

	@property
	def usbPower(self):
		"""usbPower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbPower'):
			from .Demodulation_.UsbPower import UsbPower
			self._usbPower = UsbPower(self._core, self._base)
		return self._usbPower

	@property
	def lsbPower(self):
		"""lsbPower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_lsbPower'):
			from .Demodulation_.LsbPower import LsbPower
			self._lsbPower = LsbPower(self._core, self._base)
		return self._lsbPower

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
