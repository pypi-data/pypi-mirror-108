from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("marker", core, parent)
		
		self._base.multi_repcap_types = "MarkerOther,Marker"

	@property
	def placement(self):
		"""placement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_placement'):
			from .Marker_.Placement import Placement
			self._placement = Placement(self._core, self._base)
		return self._placement

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_range'):
			from .Marker_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	def clone(self) -> 'Marker':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Marker(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
