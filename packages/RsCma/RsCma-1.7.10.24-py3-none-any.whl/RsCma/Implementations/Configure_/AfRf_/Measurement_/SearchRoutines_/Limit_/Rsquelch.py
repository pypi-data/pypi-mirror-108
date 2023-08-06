from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsquelch:
	"""Rsquelch commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rsquelch", core, parent)

	# noinspection PyTypeChecker
	class TsensitivityStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: -130 dBm to -106 dBm, Unit: dBm
			- Upper: float: Range: -108 dBm to -30 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_tsensitivity(self) -> TsensitivityStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity \n
		Snippet: value: TsensitivityStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.get_tsensitivity() \n
		Enables a limit check and sets limits for the squelch off level. \n
			:return: structure: for return value, see the help for TsensitivityStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity?', self.__class__.TsensitivityStruct())

	def set_tsensitivity(self, value: TsensitivityStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.set_tsensitivity(value = TsensitivityStruct()) \n
		Enables a limit check and sets limits for the squelch off level. \n
			:param value: see the help for TsensitivityStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity', value)

	# noinspection PyTypeChecker
	class ThysteresisStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: 0.1 dB to 3.0 dB, Unit: dB
			- Upper: float: Range: 1.0 dB to 10.0 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_thysteresis(self) -> ThysteresisStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis \n
		Snippet: value: ThysteresisStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.get_thysteresis() \n
		Enables a limit check and sets limits for the squelch hysteresis result. \n
			:return: structure: for return value, see the help for ThysteresisStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis?', self.__class__.ThysteresisStruct())

	def set_thysteresis(self, value: ThysteresisStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.set_thysteresis(value = ThysteresisStruct()) \n
		Enables a limit check and sets limits for the squelch hysteresis result. \n
			:param value: see the help for ThysteresisStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis', value)
