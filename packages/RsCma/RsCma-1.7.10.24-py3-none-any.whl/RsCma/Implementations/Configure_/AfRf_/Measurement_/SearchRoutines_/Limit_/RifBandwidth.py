from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RifBandwidth:
	"""RifBandwidth commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rifBandwidth", core, parent)

	# noinspection PyTypeChecker
	class BwDisplaceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: 1 Hz to 100000 Hz, Unit: Hz
			- Upper: float: Range: 1000 Hz to 1 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_bw_displace(self) -> BwDisplaceStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace \n
		Snippet: value: BwDisplaceStruct = driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.get_bw_displace() \n
		Enables a limit check and sets limits for the RX bandwidth / RF signal displacement bandwidth. \n
			:return: structure: for return value, see the help for BwDisplaceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace?', self.__class__.BwDisplaceStruct())

	def set_bw_displace(self, value: BwDisplaceStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.set_bw_displace(value = BwDisplaceStruct()) \n
		Enables a limit check and sets limits for the RX bandwidth / RF signal displacement bandwidth. \n
			:param value: see the help for BwDisplaceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace', value)

	# noinspection PyTypeChecker
	class FoffsetStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Upper: float: Range: 1 Hz to 50000 Hz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_foffset(self) -> FoffsetStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset \n
		Snippet: value: FoffsetStruct = driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.get_foffset() \n
		Sets the upper limit for the center frequency offset. \n
			:return: structure: for return value, see the help for FoffsetStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset?', self.__class__.FoffsetStruct())

	def set_foffset(self, value: FoffsetStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.set_foffset(value = FoffsetStruct()) \n
		Sets the upper limit for the center frequency offset. \n
			:param value: see the help for FoffsetStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset', value)
