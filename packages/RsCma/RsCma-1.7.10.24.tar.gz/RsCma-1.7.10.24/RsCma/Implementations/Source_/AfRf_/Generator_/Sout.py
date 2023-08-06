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
	class LevelStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Level_Left: float: Level for the left channel Range: 0.01 % to 100 %, Unit: %
			- Level_Right: float: Level for the right channel Range: 0.01 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Level_Left'),
			ArgStruct.scalar_float('Level_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Level_Left: float = None
			self.Level_Right: float = None

	def get_level(self) -> LevelStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:LEVel \n
		Snippet: value: LevelStruct = driver.source.afRf.generator.sout.get_level() \n
		Specifies the output levels for the SPDIF OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:return: structure: for return value, see the help for LevelStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:SOUT:LEVel?', self.__class__.LevelStruct())

	def set_level(self, value: LevelStruct) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:LEVel \n
		Snippet: driver.source.afRf.generator.sout.set_level(value = LevelStruct()) \n
		Specifies the output levels for the SPDIF OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:param value: see the help for LevelStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:AFRF:GENerator<Instance>:SOUT:LEVel', value)

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left: bool: OFF | ON
			- Right: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Left'),
			ArgStruct.scalar_bool('Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left: bool = None
			self.Right: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:ENABle \n
		Snippet: value: EnableStruct = driver.source.afRf.generator.sout.get_enable() \n
		Enables or disables the left and right channel of the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:SOUT:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:ENABle \n
		Snippet: driver.source.afRf.generator.sout.set_enable(value = EnableStruct()) \n
		Enables or disables the left and right channel of the SPDIF OUT connector. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:AFRF:GENerator<Instance>:SOUT:ENABle', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Source_Left: enums.SignalSource: GEN3 | AFI1 | SPIL GEN3 Audio generator 3 AFI1 AF1 IN SPIL SPDIF IN, left channel
			- Source_Right: enums.SignalSource: GEN4 | AFI2 | SPIR GEN4 Audio generator 4 AFI2 AF2 IN SPIR SPDIF IN, right channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Source_Left', enums.SignalSource),
			ArgStruct.scalar_enum('Source_Right', enums.SignalSource)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Source_Left: enums.SignalSource = None
			self.Source_Right: enums.SignalSource = None

	# noinspection PyTypeChecker
	def get_value(self) -> ValueStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT \n
		Snippet: value: ValueStruct = driver.source.afRf.generator.sout.get_value() \n
		Selects audio signal sources for the left and right channel of the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:SOUT?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT \n
		Snippet: driver.source.afRf.generator.sout.set_value(value = ValueStruct()) \n
		Selects audio signal sources for the left and right channel of the SPDIF OUT connector. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:AFRF:GENerator<Instance>:SOUT', value)
