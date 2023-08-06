from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCarrier:
	"""RfCarrier commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfCarrier", core, parent)

	# noinspection PyTypeChecker
	class FreqErrorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Limit: float: Range: 1 Hz to 1 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_freq_error(self) -> FreqErrorStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:FERRor \n
		Snippet: value: FreqErrorStruct = driver.configure.vse.measurement.limit.rfCarrier.get_freq_error() \n
		Configures an upper limit for the measured RF carrier frequency error. \n
			:return: structure: for return value, see the help for FreqErrorStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:FERRor?', self.__class__.FreqErrorStruct())

	def set_freq_error(self, value: FreqErrorStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:FERRor \n
		Snippet: driver.configure.vse.measurement.limit.rfCarrier.set_freq_error(value = FreqErrorStruct()) \n
		Configures an upper limit for the measured RF carrier frequency error. \n
			:param value: see the help for FreqErrorStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:FERRor', value)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			- Upper: float: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_power(self) -> PowerStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer \n
		Snippet: value: PowerStruct = driver.configure.vse.measurement.limit.rfCarrier.get_power() \n
		Configures limits for the measured RF power (PEP) . \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer \n
		Snippet: driver.configure.vse.measurement.limit.rfCarrier.set_power(value = PowerStruct()) \n
		Configures limits for the measured RF power (PEP) . \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer', value)
