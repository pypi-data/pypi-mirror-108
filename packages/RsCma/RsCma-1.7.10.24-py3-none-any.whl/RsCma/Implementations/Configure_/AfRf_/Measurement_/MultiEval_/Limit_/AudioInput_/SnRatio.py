from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SnRatio:
	"""SnRatio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("snRatio", core, parent)

	# noinspection PyTypeChecker
	class SnRatioStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower limit Range: 1 dB to 46 dB, Unit: dB
			- Upper: float: Optional setting parameter. Upper limit Range: 1 dB to 46 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def set(self, structure: SnRatioStruct, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.audioInput.snRatio.set(value = [PROPERTY_STRUCT_NAME](), audioInput = repcap.AudioInput.Default) \n
		Configures limits for all SNR results, measured via an AF input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:param structure: for set value, see the help for SnRatioStruct structure arguments.
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SNRatio', structure)

	def get(self, audioInput=repcap.AudioInput.Default) -> SnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SNRatio \n
		Snippet: value: SnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.audioInput.snRatio.get(audioInput = repcap.AudioInput.Default) \n
		Configures limits for all SNR results, measured via an AF input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for SnRatioStruct structure arguments."""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SNRatio?', self.__class__.SnRatioStruct())
