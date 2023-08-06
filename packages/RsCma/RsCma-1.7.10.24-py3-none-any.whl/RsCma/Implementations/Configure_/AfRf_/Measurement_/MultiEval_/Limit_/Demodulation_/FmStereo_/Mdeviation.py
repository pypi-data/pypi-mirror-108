from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mdeviation:
	"""Mdeviation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mdeviation", core, parent)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower multiplex deviation limit A setting configures also the upper limit (same absolute value, positive sign) . Range: -100 kHz to 0 Hz, Unit: Hz
			- Upper: float: A query returns the upper multiplex deviation limit. A setting ignores this parameter. Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_peak(self) -> PeakStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK \n
		Snippet: value: PeakStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.get_peak() \n
		Configures limits for the multiplex deviation results '+Peak' and '-Peak', measured for FM stereo. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.set_peak(value = PeakStruct()) \n
		Configures limits for the multiplex deviation results '+Peak' and '-Peak', measured for FM stereo. \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK', value)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper multiplex deviation limit Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:RMS \n
		Snippet: value: RmsStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.get_rms() \n
		Configures a limit for the 'RMS' multiplex deviation results, measured for FM stereo. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:RMS \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.set_rms(value = RmsStruct()) \n
		Configures a limit for the 'RMS' multiplex deviation results, measured for FM stereo. \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:RMS', value)
