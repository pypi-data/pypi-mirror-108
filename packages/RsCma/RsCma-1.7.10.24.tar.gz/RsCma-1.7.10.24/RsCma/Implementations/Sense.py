from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sense:
	"""Sense commands group definition. 17 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sense", core, parent)

	@property
	def base(self):
		"""base commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_base'):
			from .Sense_.Base import Base
			self._base = Base(self._core, self._base)
		return self._base

	@property
	def sequencer(self):
		"""sequencer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sense_.Sequencer import Sequencer
			self._sequencer = Sequencer(self._core, self._base)
		return self._sequencer

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Sense_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def firmwareUpdate(self):
		"""firmwareUpdate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_firmwareUpdate'):
			from .Sense_.FirmwareUpdate import FirmwareUpdate
			self._firmwareUpdate = FirmwareUpdate(self._core, self._base)
		return self._firmwareUpdate

	def clone(self) -> 'Sense':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sense(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
