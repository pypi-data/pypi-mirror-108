from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FftSpecAn:
	"""FftSpecAn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fftSpecAn", core, parent)

	# noinspection PyTypeChecker
	class TraceStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Trace_Enable: bool: OFF | ON Disables or enables the trace/diagrams selected via Trace
			- Trace: enums.TraceB: Optional setting parameter. CURRent | AVERage | MAXimum | MINimum | TDOMmain Selects the trace (current, average, max, min) or diagrams (time domain) to be enabled/disabled To enable or disable all traces and diagrams, omit the parameter."""
		__meta_args_list = [
			ArgStruct.scalar_bool('Trace_Enable'),
			ArgStruct.scalar_enum_optional('Trace', enums.TraceB)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trace_Enable: bool = None
			self.Trace: enums.TraceB = None

	def set_trace(self, value: TraceStruct) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:FFTSanalyzer:TRACe \n
		Snippet: driver.display.gprfMeasurement.fftSpecAn.set_trace(value = TraceStruct()) \n
		Selects which traces and diagrams are displayed on the 'FFT Spectrum' tab. \n
			:param value: see the help for TraceStruct structure arguments.
		"""
		self._core.io.write_struct('DISPlay:GPRF:MEASurement<Instance>:FFTSanalyzer:TRACe', value)
