from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Localizer:
	"""Localizer commands group definition. 18 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("localizer", core, parent)

	@property
	def afSettings(self):
		"""afSettings commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_afSettings'):
			from .Localizer_.AfSettings import AfSettings
			self._afSettings = AfSettings(self._core, self._base)
		return self._afSettings

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Localizer_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def idSignal(self):
		"""idSignal commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_idSignal'):
			from .Localizer_.IdSignal import IdSignal
			self._idSignal = IdSignal(self._core, self._base)
		return self._idSignal

	def clone(self) -> 'Localizer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Localizer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
