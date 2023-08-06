from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcs:
	"""Dcs commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcs", core, parent)

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the timeout
			- Timeout: float: Waiting for a turn-off code is aborted after this time. Range: 0.1 s to 15 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get_timeout(self) -> TimeoutStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT \n
		Snippet: value: TimeoutStruct = driver.configure.afRf.measurement.multiEval.tones.dcs.get_timeout() \n
		Configures a timeout for completion of the first DCS measurement cycle. \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT?', self.__class__.TimeoutStruct())

	def set_timeout(self, value: TimeoutStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.set_timeout(value = TimeoutStruct()) \n
		Configures a timeout for completion of the first DCS measurement cycle. \n
			:param value: see the help for TimeoutStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT', value)

	def get_ec_word(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord \n
		Snippet: value: str = driver.configure.afRf.measurement.multiEval.tones.dcs.get_ec_word() \n
		Specifies the expected DCS code number. \n
			:return: exp_code_word: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value, see method RsCma.Source.AfRf.Generator.Tones.Dcs.cword. Range: #Q20 to #Q777
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord?')
		return trim_str_response(response)

	def set_ec_word(self, exp_code_word: str) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.set_ec_word(exp_code_word = r1) \n
		Specifies the expected DCS code number. \n
			:param exp_code_word: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value, see method RsCma.Source.AfRf.Generator.Tones.Dcs.cword. Range: #Q20 to #Q777
		"""
		param = Conversions.value_to_str(exp_code_word)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord {param}')

	def get_imodulation(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.dcs.get_imodulation() \n
		Enables or disables the inversion of the FSK demodulation polarity. \n
			:return: imodulation: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation?')
		return Conversions.str_to_bool(response)

	def set_imodulation(self, imodulation: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.set_imodulation(imodulation = False) \n
		Enables or disables the inversion of the FSK demodulation polarity. \n
			:param imodulation: OFF | ON
		"""
		param = Conversions.bool_to_str(imodulation)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation {param}')
