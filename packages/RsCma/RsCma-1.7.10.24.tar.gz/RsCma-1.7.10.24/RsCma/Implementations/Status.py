from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Status:
	"""Status commands group definition. 37 total commands, 7 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("status", core, parent)

	@property
	def queue(self):
		"""queue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_queue'):
			from .Status_.Queue import Queue
			self._queue = Queue(self._core, self._base)
		return self._queue

	@property
	def operation(self):
		"""operation commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_operation'):
			from .Status_.Operation import Operation
			self._operation = Operation(self._core, self._base)
		return self._operation

	@property
	def questionable(self):
		"""questionable commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_questionable'):
			from .Status_.Questionable import Questionable
			self._questionable = Questionable(self._core, self._base)
		return self._questionable

	@property
	def condition(self):
		"""condition commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_condition'):
			from .Status_.Condition import Condition
			self._condition = Condition(self._core, self._base)
		return self._condition

	@property
	def event(self):
		"""event commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_event'):
			from .Status_.Event import Event
			self._event = Event(self._core, self._base)
		return self._event

	@property
	def measurement(self):
		"""measurement commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_measurement'):
			from .Status_.Measurement import Measurement
			self._measurement = Measurement(self._core, self._base)
		return self._measurement

	@property
	def generator(self):
		"""generator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_generator'):
			from .Status_.Generator import Generator
			self._generator = Generator(self._core, self._base)
		return self._generator

	def preset(self) -> None:
		"""SCPI: STATus:PRESet \n
		Snippet: driver.status.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'STATus:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: STATus:PRESet \n
		Snippet: driver.status.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STATus:PRESet')

	def clone(self) -> 'Status':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Status(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
