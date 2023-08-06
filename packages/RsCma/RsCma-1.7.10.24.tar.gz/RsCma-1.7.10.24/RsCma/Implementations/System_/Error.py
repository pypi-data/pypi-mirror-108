from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Error:
	"""Error commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("error", core, parent)

	@property
	def code(self):
		"""code commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_code'):
			from .Error_.Code import Code
			self._code = Code(self._core, self._base)
		return self._code

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Error_Number: int: 0 means that the queue is empty. Positive error codes are instrument-dependent. Negative error codes are reserved by the SCPI standard.
			- Error_Text: str: String specifying the error"""
		__meta_args_list = [
			ArgStruct.scalar_int('Error_Number'),
			ArgStruct.scalar_str('Error_Text')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Error_Number: int = None
			self.Error_Text: str = None

	def get_all(self) -> AllStruct:
		"""SCPI: SYSTem:ERRor:ALL \n
		Snippet: value: AllStruct = driver.system.error.get_all() \n
		Queries and deletes all entries in the error queue. Each entry consists of an error code and a short description of the
		error. The entries are returned as comma-separated list: {<ErrorNumber>, <ErrorText>}entry 1, {<ErrorNumber>,
		<ErrorText>}entry 2, ..., {<ErrorNumber>, <ErrorText>}entry n \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:ERRor:ALL?', self.__class__.AllStruct())

	def get_count(self) -> int:
		"""SCPI: SYSTem:ERRor:COUNt \n
		Snippet: value: int = driver.system.error.get_count() \n
		Queries the number of entries in the error queue. \n
			:return: error_count: Number of entries Range: 0 to n
		"""
		response = self._core.io.query_str('SYSTem:ERRor:COUNt?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	class NextStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Error_Code: int: 0 means that the queue is empty. Positive error codes are instrument-dependent. Negative error codes are reserved by the SCPI standard.
			- Error_Description: str: String specifying the error"""
		__meta_args_list = [
			ArgStruct.scalar_int('Error_Code'),
			ArgStruct.scalar_str('Error_Description')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Error_Code: int = None
			self.Error_Description: str = None

	def get_next(self) -> NextStruct:
		"""SCPI: SYSTem:ERRor[:NEXT] \n
		Snippet: value: NextStruct = driver.system.error.get_next() \n
		Queries and deletes the oldest entry in the error queue. \n
			:return: structure: for return value, see the help for NextStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:ERRor:NEXT?', self.__class__.NextStruct())

	def clone(self) -> 'Error':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Error(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
