from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	# noinspection PyTypeChecker
	class DstrategyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Arg_0: enums.OperationMode: No parameter help available
			- Arg_1: enums.Dstrategy: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Arg_0', enums.OperationMode),
			ArgStruct.scalar_enum('Arg_1', enums.Dstrategy)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Arg_0: enums.OperationMode = None
			self.Arg_1: enums.Dstrategy = None

	# noinspection PyTypeChecker
	def get_dstrategy(self) -> DstrategyStruct:
		"""SCPI: INSTrument[:SELect]:DSTRategy \n
		Snippet: value: DstrategyStruct = driver.instrument.select.get_dstrategy() \n
		No command help available \n
			:return: structure: for return value, see the help for DstrategyStruct structure arguments.
		"""
		return self._core.io.query_struct('INSTrument:SELect:DSTRategy?', self.__class__.DstrategyStruct())

	def set_dstrategy(self, value: DstrategyStruct) -> None:
		"""SCPI: INSTrument[:SELect]:DSTRategy \n
		Snippet: driver.instrument.select.set_dstrategy(value = DstrategyStruct()) \n
		No command help available \n
			:param value: see the help for DstrategyStruct structure arguments.
		"""
		self._core.io.write_struct('INSTrument:SELect:DSTRategy', value)

	def get_value(self) -> str:
		"""SCPI: INSTrument[:SELect] \n
		Snippet: value: str = driver.instrument.select.get_value() \n
		No command help available \n
			:return: instrument: No help available
		"""
		response = self._core.io.query_str('INSTrument:SELect?')
		return trim_str_response(response)

	def set_value(self, instrument: str) -> None:
		"""SCPI: INSTrument[:SELect] \n
		Snippet: driver.instrument.select.set_value(instrument = r1) \n
		No command help available \n
			:param instrument: No help available
		"""
		param = Conversions.value_to_str(instrument)
		self._core.io.write(f'INSTrument:SELect {param}')
