from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dwidth:
	"""Dwidth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dwidth", core, parent)

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Dwidth: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth
			- Relative: enums.Relative: RELative | CONStant Bandwidth proportional to reference frequency or constant"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth: enums.PwrFilterType = None
			self.Relative: enums.Relative = None

	def set(self, structure: DwidthStruct, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.dwidth.set(value = [PROPERTY_STRUCT_NAME](), audioInput = repcap.AudioInput.Default) \n
		Configures the bandwidth of the distortion filter in an AF input path. \n
			:param structure: for set value, see the help for DwidthStruct structure arguments.
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write_struct(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:DWIDth', structure)

	def get(self, audioInput=repcap.AudioInput.Default) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.audioInput.filterPy.dwidth.get(audioInput = repcap.AudioInput.Default) \n
		Configures the bandwidth of the distortion filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for DwidthStruct structure arguments."""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:DWIDth?', self.__class__.DwidthStruct())
