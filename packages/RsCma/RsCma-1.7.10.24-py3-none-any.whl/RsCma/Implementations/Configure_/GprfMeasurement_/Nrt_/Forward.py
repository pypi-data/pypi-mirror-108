from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Forward:
	"""Forward commands group definition. 6 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("forward", core, parent)

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .Forward_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_limit'):
			from .Forward_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def clone(self) -> 'Forward':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Forward(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
