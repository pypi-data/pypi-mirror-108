from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gslope:
	"""Gslope commands group definition. 15 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gslope", core, parent)

	@property
	def afSettings(self):
		"""afSettings commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_afSettings'):
			from .Gslope_.AfSettings import AfSettings
			self._afSettings = AfSettings(self._core, self._base)
		return self._afSettings

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Gslope_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	def clone(self) -> 'Gslope':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gslope(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
