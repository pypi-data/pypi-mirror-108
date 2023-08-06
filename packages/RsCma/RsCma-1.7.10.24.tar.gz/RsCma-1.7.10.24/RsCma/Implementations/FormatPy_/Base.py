from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	# noinspection PyTypeChecker
	class DataStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Data_Type: enums.DataFormat: ASCii | REAL | BINary | HEXadecimal | OCTal ASCii Numeric data is transferred as ASCII bytes. Floating point numbers are transferred in scientific E notation. REAL Numeric data is transferred in a definite length block as IEEE floating point numbers, see 'Block data'. BINary | HEXadecimal | OCTal Numeric data is transferred in binary, hexadecimal or octal format.
			- Data_Length: int: The meaning depends on the DataType as listed below. A zero returned by a query means that the default value is used. For ASCii Decimal places of floating point numbers. That means, number of 'b' digits in the scientific notation a.bbbbbbE+ccc. Default: 6 decimal places For REAL Length of floating point numbers in bits: 32 bits = 4 bytes, format #14... 64 bits = 8 bytes, format #18... Default: 64 bits For BINary, HEXadecimal, OCTal Minimum number of digits. If the number is longer, more digits are used. If it is shorter, leading zeros are added. Default: 0, no leading zeros"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Data_Type', enums.DataFormat),
			ArgStruct.scalar_int('Data_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Data_Type: enums.DataFormat = None
			self.Data_Length: int = None

	# noinspection PyTypeChecker
	def get_data(self) -> DataStruct:
		"""SCPI: FORMat:BASE[:DATA] \n
		Snippet: value: DataStruct = driver.formatPy.base.get_data() \n
		Selects the format for numeric data transferred by the instrument, for example query results. \n
			:return: structure: for return value, see the help for DataStruct structure arguments.
		"""
		return self._core.io.query_struct('FORMat:BASE:DATA?', self.__class__.DataStruct())

	def set_data(self, value: DataStruct) -> None:
		"""SCPI: FORMat:BASE[:DATA] \n
		Snippet: driver.formatPy.base.set_data(value = DataStruct()) \n
		Selects the format for numeric data transferred by the instrument, for example query results. \n
			:param value: see the help for DataStruct structure arguments.
		"""
		self._core.io.write_struct('FORMat:BASE:DATA', value)

	# noinspection PyTypeChecker
	def get_border(self) -> enums.ByteOrder:
		"""SCPI: FORMat:BASE:BORDer \n
		Snippet: value: enums.ByteOrder = driver.formatPy.base.get_border() \n
		No command help available \n
			:return: byte_order: No help available
		"""
		response = self._core.io.query_str('FORMat:BASE:BORDer?')
		return Conversions.str_to_scalar_enum(response, enums.ByteOrder)

	def set_border(self, byte_order: enums.ByteOrder) -> None:
		"""SCPI: FORMat:BASE:BORDer \n
		Snippet: driver.formatPy.base.set_border(byte_order = enums.ByteOrder.NORMal) \n
		No command help available \n
			:param byte_order: No help available
		"""
		param = Conversions.enum_scalar_to_str(byte_order, enums.ByteOrder)
		self._core.io.write(f'FORMat:BASE:BORDer {param}')

	def get_dinterchange(self) -> bool:
		"""SCPI: FORMat:BASE:DINTerchange \n
		Snippet: value: bool = driver.formatPy.base.get_dinterchange() \n
		No command help available \n
			:return: dif_format: No help available
		"""
		response = self._core.io.query_str('FORMat:BASE:DINTerchange?')
		return Conversions.str_to_bool(response)

	def set_dinterchange(self, dif_format: bool) -> None:
		"""SCPI: FORMat:BASE:DINTerchange \n
		Snippet: driver.formatPy.base.set_dinterchange(dif_format = False) \n
		No command help available \n
			:param dif_format: No help available
		"""
		param = Conversions.bool_to_str(dif_format)
		self._core.io.write(f'FORMat:BASE:DINTerchange {param}')

	# noinspection PyTypeChecker
	def get_sregister(self) -> enums.StatRegFormat:
		"""SCPI: FORMat:BASE:SREGister \n
		Snippet: value: enums.StatRegFormat = driver.formatPy.base.get_sregister() \n
		No command help available \n
			:return: status_register_format: No help available
		"""
		response = self._core.io.query_str('FORMat:BASE:SREGister?')
		return Conversions.str_to_scalar_enum(response, enums.StatRegFormat)

	def set_sregister(self, status_register_format: enums.StatRegFormat) -> None:
		"""SCPI: FORMat:BASE:SREGister \n
		Snippet: driver.formatPy.base.set_sregister(status_register_format = enums.StatRegFormat.ASCii) \n
		No command help available \n
			:param status_register_format: No help available
		"""
		param = Conversions.enum_scalar_to_str(status_register_format, enums.StatRegFormat)
		self._core.io.write(f'FORMat:BASE:SREGister {param}')
