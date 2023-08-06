from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Evm:
	"""Evm commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("evm", core, parent)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Limit: float: Range: 0 FS to 1 FS, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:RMS \n
		Snippet: value: RmsStruct = driver.configure.vse.measurement.limit.tetra.evm.get_rms() \n
		Enables/disables limit evaluation and sets the upper limit for the EVM RMS result. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:RMS \n
		Snippet: driver.configure.vse.measurement.limit.tetra.evm.set_rms(value = RmsStruct()) \n
		Enables/disables limit evaluation and sets the upper limit for the EVM RMS result. \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:RMS', value)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Limit: float: Range: 0 FS to 1 FS, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_peak(self) -> PeakStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:PEAK \n
		Snippet: value: PeakStruct = driver.configure.vse.measurement.limit.tetra.evm.get_peak() \n
		Enables/disables limit evaluation and sets the upper limit for the EVM peak result. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:PEAK \n
		Snippet: driver.configure.vse.measurement.limit.tetra.evm.set_peak(value = PeakStruct()) \n
		Enables/disables limit evaluation and sets the upper limit for the EVM peak result. \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:TETRa:EVM:PEAK', value)
