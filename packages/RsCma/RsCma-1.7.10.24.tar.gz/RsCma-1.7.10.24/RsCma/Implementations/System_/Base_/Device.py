from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("device", core, parent)

	def get_id(self) -> str:
		"""SCPI: SYSTem:BASE:DEVice:ID \n
		Snippet: value: str = driver.system.base.device.get_id() \n
		No command help available \n
			:return: device_id: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DEVice:ID?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class LicenseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sw_Option: List[str]: No parameter help available
			- License_Count: List[int]: No parameter help available
			- Instrument: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Sw_Option', DataType.StringList, None, False, True, 1),
			ArgStruct('License_Count', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Instrument', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sw_Option: List[str] = None
			self.License_Count: List[int] = None
			self.Instrument: List[int] = None

	def get_license(self) -> LicenseStruct:
		"""SCPI: SYSTem:BASE:DEVice:LICense \n
		Snippet: value: LicenseStruct = driver.system.base.device.get_license() \n
		No command help available \n
			:return: structure: for return value, see the help for LicenseStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:BASE:DEVice:LICense?', self.__class__.LicenseStruct())

	def set_license(self, value: LicenseStruct) -> None:
		"""SCPI: SYSTem:BASE:DEVice:LICense \n
		Snippet: driver.system.base.device.set_license(value = LicenseStruct()) \n
		No command help available \n
			:param value: see the help for LicenseStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:BASE:DEVice:LICense', value)

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Absolute_Item_Name: List[str]: No parameter help available
			- Instrument: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Absolute_Item_Name', DataType.StringList, None, False, True, 1),
			ArgStruct('Instrument', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Absolute_Item_Name: List[str] = None
			self.Instrument: List[int] = None

	def get_setup(self) -> SetupStruct:
		"""SCPI: SYSTem:BASE:DEVice:SETup \n
		Snippet: value: SetupStruct = driver.system.base.device.get_setup() \n
		No command help available \n
			:return: structure: for return value, see the help for SetupStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:BASE:DEVice:SETup?', self.__class__.SetupStruct())

	def set_setup(self, value: SetupStruct) -> None:
		"""SCPI: SYSTem:BASE:DEVice:SETup \n
		Snippet: driver.system.base.device.set_setup(value = SetupStruct()) \n
		No command help available \n
			:param value: see the help for SetupStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:BASE:DEVice:SETup', value)
