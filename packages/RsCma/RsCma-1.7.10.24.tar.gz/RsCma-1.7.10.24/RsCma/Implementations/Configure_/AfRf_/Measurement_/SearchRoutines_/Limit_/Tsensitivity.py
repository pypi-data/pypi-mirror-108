from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tsensitivity:
	"""Tsensitivity commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tsensitivity", core, parent)

	@property
	def audioOutput(self):
		"""audioOutput commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_audioOutput'):
			from .Tsensitivity_.AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._base)
		return self._audioOutput

	@property
	def voip(self):
		"""voip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_voip'):
			from .Tsensitivity_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	def clone(self) -> 'Tsensitivity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tsensitivity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
