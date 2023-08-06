from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCarrier:
	"""RfCarrier commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfCarrier", core, parent)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Limit: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			- Upper: float: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_power(self) -> PowerStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:POWer \n
		Snippet: value: PowerStruct = driver.configure.afRf.measurement.multiEval.limit.rfCarrier.get_power() \n
		Configures limits for the measured RF signal power (RMS value) . \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:POWer \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.rfCarrier.set_power(value = PowerStruct()) \n
		Configures limits for the measured RF signal power (RMS value) . \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:POWer', value)

	# noinspection PyTypeChecker
	class FreqErrorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Limit: bool: OFF | ON Enables or disables the limit check
			- Lower: float: A query returns the lower limit. A setting applies the absolute value to the upper limit and the absolute value plus a negative sign to the lower limit. Range: -50 kHz to 0 Hz, Unit: Hz
			- Upper: float: A query returns the upper limit. A setting ignores this parameter. Range: 0 Hz to 50 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_freq_error(self) -> FreqErrorStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor \n
		Snippet: value: FreqErrorStruct = driver.configure.afRf.measurement.multiEval.limit.rfCarrier.get_freq_error() \n
		Configures limits for the measured RF carrier frequency error. The upper and lower limits have the same absolute value
		but different signs. \n
			:return: structure: for return value, see the help for FreqErrorStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor?', self.__class__.FreqErrorStruct())

	def set_freq_error(self, value: FreqErrorStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.rfCarrier.set_freq_error(value = FreqErrorStruct()) \n
		Configures limits for the measured RF carrier frequency error. The upper and lower limits have the same absolute value
		but different signs. \n
			:param value: see the help for FreqErrorStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor', value)
