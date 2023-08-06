from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scal:
	"""Scal commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scal", core, parent)

	# noinspection PyTypeChecker
	class FdeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower frequency-deviation limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper frequency-deviation limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_fdeviation(self) -> FdeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:FDEViation \n
		Snippet: value: FdeviationStruct = driver.configure.afRf.measurement.multiEval.limit.tones.scal.get_fdeviation() \n
		Configures limits for the frequency deviation of tones in an analyzed SELCAL sequence. \n
			:return: structure: for return value, see the help for FdeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:FDEViation?', self.__class__.FdeviationStruct())

	def set_fdeviation(self, value: FdeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:FDEViation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.scal.set_fdeviation(value = FdeviationStruct()) \n
		Configures limits for the frequency deviation of tones in an analyzed SELCAL sequence. \n
			:param value: see the help for FdeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:FDEViation', value)

	# noinspection PyTypeChecker
	class TtimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower tone-duration limit Range: 0.1 s to 1 s, Unit: s
			- Upper: float: Upper tone-duration limit Range: 1 s to 3 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_ttime(self) -> TtimeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TTIMe \n
		Snippet: value: TtimeStruct = driver.configure.afRf.measurement.multiEval.limit.tones.scal.get_ttime() \n
		Configures limits for the tone duration in an analyzed SELCAL sequence. \n
			:return: structure: for return value, see the help for TtimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TTIMe?', self.__class__.TtimeStruct())

	def set_ttime(self, value: TtimeStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TTIMe \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.scal.set_ttime(value = TtimeStruct()) \n
		Configures limits for the tone duration in an analyzed SELCAL sequence. \n
			:param value: see the help for TtimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TTIMe', value)

	# noinspection PyTypeChecker
	class TpauseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower pause limit Range: 0.1 s to 0.25 s, Unit: s
			- Upper: float: Upper pause limit Range: 0.25 s to 3 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_tpause(self) -> TpauseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse \n
		Snippet: value: TpauseStruct = driver.configure.afRf.measurement.multiEval.limit.tones.scal.get_tpause() \n
		Configures limits for the pause between two dual tones of an analyzed SELCAL sequence. \n
			:return: structure: for return value, see the help for TpauseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse?', self.__class__.TpauseStruct())

	def set_tpause(self, value: TpauseStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.scal.set_tpause(value = TpauseStruct()) \n
		Configures limits for the pause between two dual tones of an analyzed SELCAL sequence. \n
			:param value: see the help for TpauseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse', value)
