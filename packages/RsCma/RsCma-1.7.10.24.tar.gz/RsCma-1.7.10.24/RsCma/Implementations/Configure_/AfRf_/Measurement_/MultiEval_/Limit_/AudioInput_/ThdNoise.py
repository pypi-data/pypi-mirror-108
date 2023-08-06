from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ThdNoise:
	"""ThdNoise commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("thdNoise", core, parent)

	# noinspection PyTypeChecker
	class ThdNoiseStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper THD+N limit Range: 0.001 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def set(self, structure: ThdNoiseStruct, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:THDNoise \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.audioInput.thdNoise.set(value = [PROPERTY_STRUCT_NAME](), audioInput = repcap.AudioInput.Default) \n
		Configures a limit for the THD+N results, measured via an AF input path. \n
			:param structure: for set value, see the help for ThdNoiseStruct structure arguments.
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:THDNoise', structure)

	def get(self, audioInput=repcap.AudioInput.Default) -> ThdNoiseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:THDNoise \n
		Snippet: value: ThdNoiseStruct = driver.configure.afRf.measurement.multiEval.limit.audioInput.thdNoise.get(audioInput = repcap.AudioInput.Default) \n
		Configures a limit for the THD+N results, measured via an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for ThdNoiseStruct structure arguments."""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:THDNoise?', self.__class__.ThdNoiseStruct())
