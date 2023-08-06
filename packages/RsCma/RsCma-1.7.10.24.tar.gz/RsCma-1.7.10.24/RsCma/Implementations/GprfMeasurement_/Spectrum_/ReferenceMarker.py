from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceMarker:
	"""ReferenceMarker commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("referenceMarker", core, parent)

	@property
	def speak(self):
		"""speak commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speak'):
			from .ReferenceMarker_.Speak import Speak
			self._speak = Speak(self._core, self._base)
		return self._speak

	@property
	def npeak(self):
		"""npeak commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npeak'):
			from .ReferenceMarker_.Npeak import Npeak
			self._npeak = Npeak(self._core, self._base)
		return self._npeak

	def clone(self) -> 'ReferenceMarker':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ReferenceMarker(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
