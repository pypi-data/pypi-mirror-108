from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfRf:
	"""AfRf commands group definition. 240 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("afRf", core, parent)

	@property
	def generator(self):
		"""generator commands group. 23 Sub-classes, 2 commands."""
		if not hasattr(self, '_generator'):
			from .AfRf_.Generator import Generator
			self._generator = Generator(self._core, self._base)
		return self._generator

	def clone(self) -> 'AfRf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AfRf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
