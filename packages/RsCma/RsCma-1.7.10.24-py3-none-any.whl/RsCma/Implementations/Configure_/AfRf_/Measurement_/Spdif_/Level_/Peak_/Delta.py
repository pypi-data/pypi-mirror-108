from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delta", core, parent)

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Delta_.Update import Update
			self._update = Update(self._core, self._base)
		return self._update

	# noinspection PyTypeChecker
	class MeasuredStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left_Meas_Val: float: No parameter help available
			- Right_Meas_Val: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_Meas_Val'),
			ArgStruct.scalar_float('Right_Meas_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_Meas_Val: float = None
			self.Right_Meas_Val: float = None

	def get_measured(self) -> MeasuredStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MEASured \n
		Snippet: value: MeasuredStruct = driver.configure.afRf.measurement.spdif.level.peak.delta.get_measured() \n
		No command help available \n
			:return: structure: for return value, see the help for MeasuredStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MEASured?', self.__class__.MeasuredStruct())

	# noinspection PyTypeChecker
	class UserStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left_User_Val: float: No parameter help available
			- Right_User_Val: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_User_Val'),
			ArgStruct.scalar_float('Right_User_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_User_Val: float = None
			self.Right_User_Val: float = None

	def get_user(self) -> UserStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER \n
		Snippet: value: UserStruct = driver.configure.afRf.measurement.spdif.level.peak.delta.get_user() \n
		No command help available \n
			:return: structure: for return value, see the help for UserStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER?', self.__class__.UserStruct())

	def set_user(self, value: UserStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.spdif.level.peak.delta.set_user(value = UserStruct()) \n
		No command help available \n
			:param value: see the help for UserStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER', value)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DeltaMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MODE \n
		Snippet: value: enums.DeltaMode = driver.configure.afRf.measurement.spdif.level.peak.delta.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DeltaMode)

	def set_mode(self, mode: enums.DeltaMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MODE \n
		Snippet: driver.configure.afRf.measurement.spdif.level.peak.delta.set_mode(mode = enums.DeltaMode.MEAS) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DeltaMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:MODE {param}')

	def clone(self) -> 'Delta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
