from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdeviation:
	"""Pdeviation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pdeviation", core, parent)

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: A query returns the lower limit. A setting applies the absolute value to the upper limit and the absolute value plus a negative sign to the lower limit. Range: -10 rad to 0 rad, Unit: rad
			- Upper: float: A query returns the upper limit. A setting ignores this parameter. Range: 0 rad to 10 rad, Unit: rad"""
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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:PEAK \n
		Snippet: value: PeakStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.get_peak() \n
		Configures limits for the phase deviation results '+Peak' and '-Peak', measured for PM. The upper and lower limits have
		the same absolute value but different signs. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:PEAK?', self.__class__.PeakStruct())

	def set_peak(self, value: PeakStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:PEAK \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.set_peak(value = PeakStruct()) \n
		Configures limits for the phase deviation results '+Peak' and '-Peak', measured for PM. The upper and lower limits have
		the same absolute value but different signs. \n
			:param value: see the help for PeakStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:PEAK', value)

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper phase deviation limit Range: 0 rad to 10 rad, Unit: rad"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_rms(self) -> RmsStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS \n
		Snippet: value: RmsStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.get_rms() \n
		Configures a limit for the 'RMS' phase deviation results, measured for PM. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS?', self.__class__.RmsStruct())

	def set_rms(self, value: RmsStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.set_rms(value = RmsStruct()) \n
		Configures a limit for the 'RMS' phase deviation results, measured for PM. \n
			:param value: see the help for RmsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS', value)
