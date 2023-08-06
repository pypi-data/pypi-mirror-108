from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Samples:
	"""Samples commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("samples", core, parent)

	# noinspection PyTypeChecker
	class RangeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Range_Py: enums.ArbSamplesRange: No parameter help available
			- Start: int: No parameter help available
			- Stop: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Range_Py', enums.ArbSamplesRange),
			ArgStruct.scalar_int('Start'),
			ArgStruct.scalar_int('Stop')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Range_Py: enums.ArbSamplesRange = None
			self.Start: int = None
			self.Stop: int = None

	# noinspection PyTypeChecker
	def get_range(self) -> RangeStruct:
		"""SCPI: SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: value: RangeStruct = driver.source.xrt.generator.arb.samples.get_range() \n
		No command help available \n
			:return: structure: for return value, see the help for RangeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe?', self.__class__.RangeStruct())

	def set_range(self, value: RangeStruct) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: driver.source.xrt.generator.arb.samples.set_range(value = RangeStruct()) \n
		No command help available \n
			:param value: see the help for RangeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe', value)

	def get_value(self) -> float:
		"""SCPI: SOURce:XRT:GENerator<Instance>:ARB:SAMPles \n
		Snippet: value: float = driver.source.xrt.generator.arb.samples.get_value() \n
		No command help available \n
			:return: samples: No help available
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:ARB:SAMPles?')
		return Conversions.str_to_float(response)
