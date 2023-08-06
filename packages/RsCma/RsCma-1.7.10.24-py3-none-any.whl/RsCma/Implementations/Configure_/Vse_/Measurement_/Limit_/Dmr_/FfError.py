from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FfError:
	"""FfError commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ffError", core, parent)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Limit: float: Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_peak(self) -> PeakStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:PEAK \n
		Snippet: value: PeakStruct = driver.configure.vse.measurement.limit.dmr.ffError.get_peak() \n
		Configures an upper limit for the measured peak value of the frequency deviation error. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:PEAK \n
		Snippet: driver.configure.vse.measurement.limit.dmr.ffError.set_peak(value = PeakStruct()) \n
		Configures an upper limit for the measured peak value of the frequency deviation error. \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:PEAK', value)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Limit: float: Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:RMS \n
		Snippet: value: RmsStruct = driver.configure.vse.measurement.limit.dmr.ffError.get_rms() \n
		Configures an upper limit for the measured RMS value of the frequency deviation error. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:RMS \n
		Snippet: driver.configure.vse.measurement.limit.dmr.ffError.set_rms(value = RmsStruct()) \n
		Configures an upper limit for the measured RMS value of the frequency deviation error. \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:DMR:FFERor:RMS', value)
