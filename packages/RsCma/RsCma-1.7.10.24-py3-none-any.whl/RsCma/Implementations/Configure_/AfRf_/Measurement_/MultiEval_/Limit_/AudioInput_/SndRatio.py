from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SndRatio:
	"""SndRatio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sndRatio", core, parent)

	# noinspection PyTypeChecker
	class SndRatioStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Lower: float: No parameter help available
			- Upper: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def set(self, structure: SndRatioStruct, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SNDRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.audioInput.sndRatio.set(value = [PROPERTY_STRUCT_NAME](), audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param structure: for set value, see the help for SndRatioStruct structure arguments.
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SNDRatio', structure)

	def get(self, audioInput=repcap.AudioInput.Default) -> SndRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SNDRatio \n
		Snippet: value: SndRatioStruct = driver.configure.afRf.measurement.multiEval.limit.audioInput.sndRatio.get(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for SndRatioStruct structure arguments."""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SNDRatio?', self.__class__.SndRatioStruct())
