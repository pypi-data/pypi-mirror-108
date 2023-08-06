from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delta", core, parent)

	# noinspection PyTypeChecker
	class UserStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left_User_Val: float: Unit: Hz
			- Right_User_Val: float: Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_User_Val'),
			ArgStruct.scalar_float('Right_User_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_User_Val: float = None
			self.Right_User_Val: float = None

	def get_user(self) -> UserStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:USER \n
		Snippet: value: UserStruct = driver.configure.afRf.measurement.demodulation.fmStereo.frequency.delta.get_user() \n
		No command help available \n
			:return: structure: for return value, see the help for UserStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:USER?', self.__class__.UserStruct())

	def set_user(self, value: UserStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.demodulation.fmStereo.frequency.delta.set_user(value = UserStruct()) \n
		No command help available \n
			:param value: see the help for UserStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:USER', value)

	# noinspection PyTypeChecker
	class MeasuredStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left_Meas_Val: float: Unit: Hz
			- Right_Meas_Val: float: Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_Meas_Val'),
			ArgStruct.scalar_float('Right_Meas_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_Meas_Val: float = None
			self.Right_Meas_Val: float = None

	def get_measured(self) -> MeasuredStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:MEASured \n
		Snippet: value: MeasuredStruct = driver.configure.afRf.measurement.demodulation.fmStereo.frequency.delta.get_measured() \n
		No command help available \n
			:return: structure: for return value, see the help for MeasuredStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:MEASured?', self.__class__.MeasuredStruct())
