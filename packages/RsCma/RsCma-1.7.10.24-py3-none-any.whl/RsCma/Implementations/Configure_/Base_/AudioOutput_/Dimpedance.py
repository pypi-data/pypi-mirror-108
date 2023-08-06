from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dimpedance:
	"""Dimpedance commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dimpedance", core, parent)

	# noinspection PyTypeChecker
	class DimpedanceStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable: bool: OFF | ON ON: Use the configured Impedance. OFF: Ignore the configured Impedance.
			- Impedance: float: Range: 1 Ω to 100E+6 Ω, Unit: Ω"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Impedance')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Impedance: float = None

	def set(self, structure: DimpedanceStruct, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:BASE:AOUT<nr>:DIMPedance \n
		Snippet: driver.configure.base.audioOutput.dimpedance.set(value = [PROPERTY_STRUCT_NAME](), audioOutput = repcap.AudioOutput.Default) \n
		Configures the impedance 'Rin DUT' for passive circuitry. \n
			:param structure: for set value, see the help for DimpedanceStruct structure arguments.
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')"""
		audioOutput_cmd_val = self._base.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write_struct(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:DIMPedance', structure)

	def get(self, audioOutput=repcap.AudioOutput.Default) -> DimpedanceStruct:
		"""SCPI: CONFigure:BASE:AOUT<nr>:DIMPedance \n
		Snippet: value: DimpedanceStruct = driver.configure.base.audioOutput.dimpedance.get(audioOutput = repcap.AudioOutput.Default) \n
		Configures the impedance 'Rin DUT' for passive circuitry. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: structure: for return value, see the help for DimpedanceStruct structure arguments."""
		audioOutput_cmd_val = self._base.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		return self._core.io.query_struct(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:DIMPedance?', self.__class__.DimpedanceStruct())
