from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 26 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def dmr(self):
		"""dmr commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr'):
			from .Limit_.Dmr import Dmr
			self._dmr = Dmr(self._core, self._base)
		return self._dmr

	@property
	def dpmr(self):
		"""dpmr commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpmr'):
			from .Limit_.Dpmr import Dpmr
			self._dpmr = Dpmr(self._core, self._base)
		return self._dpmr

	@property
	def nxdn(self):
		"""nxdn commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_nxdn'):
			from .Limit_.Nxdn import Nxdn
			self._nxdn = Nxdn(self._core, self._base)
		return self._nxdn

	@property
	def tetra(self):
		"""tetra commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tetra'):
			from .Limit_.Tetra import Tetra
			self._tetra = Tetra(self._core, self._base)
		return self._tetra

	@property
	def ptFive(self):
		"""ptFive commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptFive'):
			from .Limit_.PtFive import PtFive
			self._ptFive = PtFive(self._core, self._base)
		return self._ptFive

	@property
	def rfCarrier(self):
		"""rfCarrier commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfCarrier'):
			from .Limit_.RfCarrier import RfCarrier
			self._rfCarrier = RfCarrier(self._core, self._base)
		return self._rfCarrier

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
