from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Filter_Left_Enable: bool: No parameter help available
			- Filter_Right_Enable: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Filter_Left_Enable'),
			ArgStruct.scalar_bool('Filter_Right_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left_Enable: bool = None
			self.Filter_Right_Enable: bool = None

	def set(self, structure: EnableStruct, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:ENABle \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.notch.enable.set(value = [PROPERTY_STRUCT_NAME](), notch = repcap.Notch.Default) \n
		No command help available \n
			:param structure: for set value, see the help for EnableStruct structure arguments.
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:ENABle', structure)

	def get(self, notch=repcap.Notch.Default) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.spdif.filterPy.notch.enable.get(notch = repcap.Notch.Default) \n
		No command help available \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:ENABle?', self.__class__.EnableStruct())
