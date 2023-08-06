from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 8 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def rsensitivity(self):
		"""rsensitivity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsensitivity'):
			from .Limit_.Rsensitivity import Rsensitivity
			self._rsensitivity = Rsensitivity(self._core, self._base)
		return self._rsensitivity

	@property
	def rifBandwidth(self):
		"""rifBandwidth commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rifBandwidth'):
			from .Limit_.RifBandwidth import RifBandwidth
			self._rifBandwidth = RifBandwidth(self._core, self._base)
		return self._rifBandwidth

	@property
	def rsquelch(self):
		"""rsquelch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rsquelch'):
			from .Limit_.Rsquelch import Rsquelch
			self._rsquelch = Rsquelch(self._core, self._base)
		return self._rsquelch

	@property
	def tsensitivity(self):
		"""tsensitivity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsensitivity'):
			from .Limit_.Tsensitivity import Tsensitivity
			self._tsensitivity = Tsensitivity(self._core, self._base)
		return self._tsensitivity

	# noinspection PyTypeChecker
	class SsnrStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Upper: float: Unit: dB
			- Lower: float: Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper'),
			ArgStruct.scalar_float('Lower')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None
			self.Lower: float = None

	def get_ssnr(self) -> SsnrStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR \n
		Snippet: value: SsnrStruct = driver.configure.afRf.measurement.searchRoutines.limit.get_ssnr() \n
		Enables a limit check and sets limits for the determined SNR. \n
			:return: structure: for return value, see the help for SsnrStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR?', self.__class__.SsnrStruct())

	def set_ssnr(self, value: SsnrStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.set_ssnr(value = SsnrStruct()) \n
		Enables a limit check and sets limits for the determined SNR. \n
			:param value: see the help for SsnrStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR', value)

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
