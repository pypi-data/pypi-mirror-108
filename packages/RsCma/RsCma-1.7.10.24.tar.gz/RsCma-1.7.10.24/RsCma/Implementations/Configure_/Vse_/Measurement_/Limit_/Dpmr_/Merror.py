from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Merror:
	"""Merror commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("merror", core, parent)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Limit: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:RMS \n
		Snippet: value: RmsStruct = driver.configure.vse.measurement.limit.dpmr.merror.get_rms() \n
		No command help available \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:RMS \n
		Snippet: driver.configure.vse.measurement.limit.dpmr.merror.set_rms(value = RmsStruct()) \n
		No command help available \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:RMS', value)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Limit: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_peak(self) -> PeakStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:PEAK \n
		Snippet: value: PeakStruct = driver.configure.vse.measurement.limit.dpmr.merror.get_peak() \n
		No command help available \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:PEAK \n
		Snippet: driver.configure.vse.measurement.limit.dpmr.merror.set_peak(value = PeakStruct()) \n
		No command help available \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:MERRor:PEAK', value)
