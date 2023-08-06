from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Frequency_1: float: No parameter help available
			- Frequency_2: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_1'),
			ArgStruct.scalar_float('Frequency_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_1: float = None
			self.Frequency_2: float = None

	def set(self, structure: FrequencyStruct, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DTONe:FREQuency \n
		Snippet: driver.source.afRf.generator.internalGenerator.dtone.frequency.set(value = [PROPERTY_STRUCT_NAME](), internalGen = repcap.InternalGen.Default) \n
		No command help available \n
			:param structure: for set value, see the help for FrequencyStruct structure arguments.
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')"""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write_struct(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DTONe:FREQuency', structure)

	def get(self, internalGen=repcap.InternalGen.Default) -> FrequencyStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DTONe:FREQuency \n
		Snippet: value: FrequencyStruct = driver.source.afRf.generator.internalGenerator.dtone.frequency.get(internalGen = repcap.InternalGen.Default) \n
		No command help available \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: structure: for return value, see the help for FrequencyStruct structure arguments."""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DTONe:FREQuency?', self.__class__.FrequencyStruct())
