from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sout:
	"""Sout commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sout", core, parent)

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Switches the left channel off or on
			- Enable_Right: bool: OFF | ON Switches the right channel off or on"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_bool('Enable_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Enable_Right: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.sout.get_enable() \n
		Enables or disables the channels of the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle \n
		Snippet: driver.configure.afRf.measurement.sout.set_enable(value = EnableStruct()) \n
		Enables or disables the channels of the SPDIF OUT connector. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle', value)

	# noinspection PyTypeChecker
	class SourceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Source_Left: enums.AudioSource: DEM | DEML Source for the left SPDIF channel DEM Demodulator output (FM, PM, ...) DEML Demodulator output, left channel (FM stereo)
			- Source_Right: enums.AudioSource: DEM | DEMR Source for the right SPDIF channel DEM Demodulator output (FM, PM, ...) DEMR Demodulator output, right channel (FM stereo)"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Source_Left', enums.AudioSource),
			ArgStruct.scalar_enum('Source_Right', enums.AudioSource)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Source_Left: enums.AudioSource = None
			self.Source_Right: enums.AudioSource = None

	# noinspection PyTypeChecker
	def get_source(self) -> SourceStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:SOURce \n
		Snippet: value: SourceStruct = driver.configure.afRf.measurement.sout.get_source() \n
		Queries the audio signal sources for the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for SourceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:SOURce?', self.__class__.SourceStruct())

	# noinspection PyTypeChecker
	class LevelStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Level_Left: float: Level for the left channel Unit: %
			- Level_Right: float: Level for the right channel Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Level_Left'),
			ArgStruct.scalar_float('Level_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Level_Left: float = None
			self.Level_Right: float = None

	def get_level(self) -> LevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel \n
		Snippet: value: LevelStruct = driver.configure.afRf.measurement.sout.get_level() \n
		Specifies the output levels for the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for LevelStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel?', self.__class__.LevelStruct())

	def set_level(self, value: LevelStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel \n
		Snippet: driver.configure.afRf.measurement.sout.set_level(value = LevelStruct()) \n
		Specifies the output levels for the SPDIF OUT connector. \n
			:param value: see the help for LevelStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel', value)
