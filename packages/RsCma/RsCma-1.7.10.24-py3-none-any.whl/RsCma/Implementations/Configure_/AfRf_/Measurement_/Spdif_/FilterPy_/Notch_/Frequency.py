from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Filter_Left_Frequency: float: No parameter help available
			- Filter_Right_Frequency: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Filter_Left_Frequency'),
			ArgStruct.scalar_float('Filter_Right_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left_Frequency: float = None
			self.Filter_Right_Frequency: float = None

	def set(self, structure: FrequencyStruct, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.notch.frequency.set(value = [PROPERTY_STRUCT_NAME](), notch = repcap.Notch.Default) \n
		No command help available \n
			:param structure: for set value, see the help for FrequencyStruct structure arguments.
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:FREQuency', structure)

	def get(self, notch=repcap.Notch.Default) -> FrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: value: FrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.notch.frequency.get(notch = repcap.Notch.Default) \n
		No command help available \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: structure: for return value, see the help for FrequencyStruct structure arguments."""
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:FREQuency?', self.__class__.FrequencyStruct())
