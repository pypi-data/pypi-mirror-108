from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("range", core, parent)

	# noinspection PyTypeChecker
	class RangeStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Xrange_Lower: float: Range: 0 s to SweepTime, Unit: s
			- Xrange_Upper: float: Range: 0 s to SweepTime, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_float('Xrange_Lower'),
			ArgStruct.scalar_float('Xrange_Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Xrange_Lower: float = None
			self.Xrange_Upper: float = None

	def set(self, structure: RangeStruct, marker=repcap.Marker.Nr1) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:RANGe \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.range.set(value = [PROPERTY_STRUCT_NAME](), marker = repcap.Marker.Nr1) \n
		Specifies the peak search range, for marker number <no> and zero span mode. Marker number one is the reference marker. \n
			:param structure: for set value, see the help for RangeStruct structure arguments.
			:param marker: optional repeated capability selector. Default value: Nr1"""
		marker_cmd_val = self._base.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write_struct(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{marker_cmd_val}:RANGe', structure)

	def get(self, marker=repcap.Marker.Nr1) -> RangeStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:RANGe \n
		Snippet: value: RangeStruct = driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.range.get(marker = repcap.Marker.Nr1) \n
		Specifies the peak search range, for marker number <no> and zero span mode. Marker number one is the reference marker. \n
			:param marker: optional repeated capability selector. Default value: Nr1
			:return: structure: for return value, see the help for RangeStruct structure arguments."""
		marker_cmd_val = self._base.get_repcap_cmd_value(marker, repcap.Marker)
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{marker_cmd_val}:RANGe?', self.__class__.RangeStruct())
