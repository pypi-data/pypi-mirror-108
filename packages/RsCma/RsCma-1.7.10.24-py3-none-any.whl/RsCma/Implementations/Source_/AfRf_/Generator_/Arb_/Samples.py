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
			- Range_Py: enums.ArbSamplesRange: FULL | SUB FULL Process all samples SUB Process a subrange according to Start and Stop
			- Start: int: Start of the subrange (always first sample, labeled zero) Range: 0 (fixed value)
			- Stop: int: End of the subrange Range: 16 to samples in ARB file - 1"""
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
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: value: RangeStruct = driver.source.afRf.generator.arb.samples.get_range() \n
		Selects whether all samples or a subrange of samples is processed. \n
			:return: structure: for return value, see the help for RangeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:ARB:SAMPles:RANGe?', self.__class__.RangeStruct())

	def set_range(self, value: RangeStruct) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: driver.source.afRf.generator.arb.samples.set_range(value = RangeStruct()) \n
		Selects whether all samples or a subrange of samples is processed. \n
			:param value: see the help for RangeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:AFRF:GENerator<Instance>:ARB:SAMPles:RANGe', value)

	def get_value(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:SAMPles \n
		Snippet: value: float = driver.source.afRf.generator.arb.samples.get_value() \n
		Queries the number of samples in the loaded ARB file. \n
			:return: samples: Range: 0 to 268173312
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:SAMPles?')
		return Conversions.str_to_float(response)
