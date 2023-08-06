from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcs:
	"""Dcs commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcs", core, parent)

	# noinspection PyTypeChecker
	class FskDeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower limit Range: -10 kHz to 0 Hz, Unit: Hz
			- Upper: float: Upper limit Range: 0 Hz to 10 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_fsk_deviation(self) -> FskDeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:FSKDeviation \n
		Snippet: value: FskDeviationStruct = driver.configure.afRf.measurement.multiEval.limit.tones.dcs.get_fsk_deviation() \n
		Configures limits for the FSK deviation measured for a DCS signal. \n
			:return: structure: for return value, see the help for FskDeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:FSKDeviation?', self.__class__.FskDeviationStruct())

	def set_fsk_deviation(self, value: FskDeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:FSKDeviation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.dcs.set_fsk_deviation(value = FskDeviationStruct()) \n
		Configures limits for the FSK deviation measured for a DCS signal. \n
			:param value: see the help for FskDeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:FSKDeviation', value)

	# noinspection PyTypeChecker
	class TocLengthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower limit Range: 0 s to 0.15 s, Unit: s
			- Upper: float: Upper limit Range: 0.15 s to 1 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_toc_length(self) -> TocLengthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOCLength \n
		Snippet: value: TocLengthStruct = driver.configure.afRf.measurement.multiEval.limit.tones.dcs.get_toc_length() \n
		Configures limits for the duration of DCS turn-off code transmissions. \n
			:return: structure: for return value, see the help for TocLengthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOCLength?', self.__class__.TocLengthStruct())

	def set_toc_length(self, value: TocLengthStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOCLength \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.dcs.set_toc_length(value = TocLengthStruct()) \n
		Configures limits for the duration of DCS turn-off code transmissions. \n
			:param value: see the help for TocLengthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOCLength', value)

	# noinspection PyTypeChecker
	class TofDeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Upper: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_tof_deviation(self) -> TofDeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOFDeviation \n
		Snippet: value: TofDeviationStruct = driver.configure.afRf.measurement.multiEval.limit.tones.dcs.get_tof_deviation() \n
		No command help available \n
			:return: structure: for return value, see the help for TofDeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOFDeviation?', self.__class__.TofDeviationStruct())

	def set_tof_deviation(self, value: TofDeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOFDeviation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.dcs.set_tof_deviation(value = TofDeviationStruct()) \n
		No command help available \n
			:param value: see the help for TofDeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DCS:TOFDeviation', value)
