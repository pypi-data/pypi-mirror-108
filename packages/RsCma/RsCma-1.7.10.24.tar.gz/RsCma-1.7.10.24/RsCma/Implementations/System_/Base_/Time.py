from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	# noinspection PyTypeChecker
	class TzoneStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: No parameter help available
			- Minute: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None

	def get_tzone(self) -> TzoneStruct:
		"""SCPI: SYSTem:BASE:TIME:TZONe \n
		Snippet: value: TzoneStruct = driver.system.base.time.get_tzone() \n
		No command help available \n
			:return: structure: for return value, see the help for TzoneStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:BASE:TIME:TZONe?', self.__class__.TzoneStruct())

	def set_tzone(self, value: TzoneStruct) -> None:
		"""SCPI: SYSTem:BASE:TIME:TZONe \n
		Snippet: driver.system.base.time.set_tzone(value = TzoneStruct()) \n
		No command help available \n
			:param value: see the help for TzoneStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:BASE:TIME:TZONe', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: No parameter help available
			- Min: int: No parameter help available
			- Sec: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Min'),
			ArgStruct.scalar_int('Sec')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Min: int = None
			self.Sec: int = None

	def get_value(self) -> ValueStruct:
		"""SCPI: SYSTem:BASE:TIME \n
		Snippet: value: ValueStruct = driver.system.base.time.get_value() \n
		No command help available \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:BASE:TIME?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: SYSTem:BASE:TIME \n
		Snippet: driver.system.base.time.set_value(value = ValueStruct()) \n
		No command help available \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:BASE:TIME', value)
