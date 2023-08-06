from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdeviation:
	"""Fdeviation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdeviation", core, parent)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: A query returns the lower limit. A setting applies the absolute value to the upper limit and the absolute value plus a negative sign to the lower limit. Range: -100 kHz to 0 Hz, Unit: Hz
			- Upper: float: A query returns the upper limit. A setting ignores this parameter. Range: 0 Hz to 100 kHz, Unit: Hz"""
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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:PEAK \n
		Snippet: value: PeakStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fdeviation.get_peak() \n
		Configures limits for the frequency deviation results '+Peak' and '-Peak', measured for FM. The upper and lower limits
		have the same absolute value but different signs. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:PEAK \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fdeviation.set_peak(value = PeakStruct()) \n
		Configures limits for the frequency deviation results '+Peak' and '-Peak', measured for FM. The upper and lower limits
		have the same absolute value but different signs. \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:PEAK', value)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper frequency deviation limit Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:RMS \n
		Snippet: value: RmsStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fdeviation.get_rms() \n
		Configures a limit for the 'RMS' frequency deviation results, measured for FM. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:RMS \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fdeviation.set_rms(value = RmsStruct()) \n
		Configures a limit for the 'RMS' frequency deviation results, measured for FM. \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FDEViation:RMS', value)
