from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dialing:
	"""Dialing commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dialing", core, parent)

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Mode: enums.TimeoutMode: No parameter help available
			- Timeout: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_enum('Mode', enums.TimeoutMode),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Mode: enums.TimeoutMode = None
			self.Timeout: float = None

	def get_timeout(self) -> TimeoutStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT \n
		Snippet: value: TimeoutStruct = driver.configure.afRf.measurement.multiEval.tones.dialing.get_timeout() \n
		No command help available \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT?', self.__class__.TimeoutStruct())

	def set_timeout(self, value: TimeoutStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dialing.set_timeout(value = TimeoutStruct()) \n
		No command help available \n
			:param value: see the help for TimeoutStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT', value)

	# noinspection PyTypeChecker
	class ToStartStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables the timeout
			- Timeout: float: Time interval during which the first tone must be detected Range: 0.8 s to 86400 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get_to_start(self) -> ToStartStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOSTart \n
		Snippet: value: ToStartStruct = driver.configure.afRf.measurement.multiEval.tones.dialing.get_to_start() \n
		Configures a timeout for the detection of the first tone during a dialing sequence analysis. \n
			:return: structure: for return value, see the help for ToStartStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOSTart?', self.__class__.ToStartStruct())

	def set_to_start(self, value: ToStartStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOSTart \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dialing.set_to_start(value = ToStartStruct()) \n
		Configures a timeout for the detection of the first tone during a dialing sequence analysis. \n
			:param value: see the help for ToStartStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOSTart', value)

	# noinspection PyTypeChecker
	class ToEndStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables the timeout
			- Timeout: float: Maximum time interval after the end of a tone and the start of the next tone Range: 0.1 s to 30 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get_to_end(self) -> ToEndStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd \n
		Snippet: value: ToEndStruct = driver.configure.afRf.measurement.multiEval.tones.dialing.get_to_end() \n
		Configures a timeout for waiting for the next tone during a dialing sequence analysis. \n
			:return: structure: for return value, see the help for ToEndStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd?', self.__class__.ToEndStruct())

	def set_to_end(self, value: ToEndStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dialing.set_to_end(value = ToEndStruct()) \n
		Configures a timeout for waiting for the next tone during a dialing sequence analysis. \n
			:param value: see the help for ToEndStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd', value)
