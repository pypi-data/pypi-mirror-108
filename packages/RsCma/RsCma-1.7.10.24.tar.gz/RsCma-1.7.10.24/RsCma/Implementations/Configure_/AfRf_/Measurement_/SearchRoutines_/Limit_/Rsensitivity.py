from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsensitivity:
	"""Rsensitivity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rsensitivity", core, parent)

	# noinspection PyTypeChecker
	class RsLevelStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper limit for the RX sensitivity Range: -120 dBm to -100 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_rs_level(self) -> RsLevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel \n
		Snippet: value: RsLevelStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsensitivity.get_rs_level() \n
		Configures an upper limit for the measured RX sensitivity. \n
			:return: structure: for return value, see the help for RsLevelStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel?', self.__class__.RsLevelStruct())

	def set_rs_level(self, value: RsLevelStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsensitivity.set_rs_level(value = RsLevelStruct()) \n
		Configures an upper limit for the measured RX sensitivity. \n
			:param value: see the help for RsLevelStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel', value)
