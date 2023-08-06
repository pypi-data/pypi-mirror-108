from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCarrier:
	"""RfCarrier commands group definition. 12 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfCarrier", core, parent)

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .RfCarrier_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def freqError(self):
		"""freqError commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqError'):
			from .RfCarrier_.FreqError import FreqError
			self._freqError = FreqError(self._core, self._base)
		return self._freqError

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .RfCarrier_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	def clone(self) -> 'RfCarrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfCarrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
