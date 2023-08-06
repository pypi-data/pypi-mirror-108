from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spectrum:
	"""Spectrum commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spectrum", core, parent)

	@property
	def application(self):
		"""application commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_application'):
			from .Spectrum_.Application import Application
			self._application = Application(self._core, self._base)
		return self._application

	# noinspection PyTypeChecker
	class TraceStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Trace_Enable: bool: OFF | ON Disables or enables the trace selected via Trace
			- Trace: enums.Statistic: Optional setting parameter. CURRent | AVERage | MAXimum | MINimum Selects the trace to be enabled/disabled To enable or disable all traces, omit the parameter."""
		__meta_args_list = [
			ArgStruct.scalar_bool('Trace_Enable'),
			ArgStruct.scalar_enum_optional('Trace', enums.Statistic)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trace_Enable: bool = None
			self.Trace: enums.Statistic = None

	def set_trace(self, value: TraceStruct) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:SPECtrum:TRACe \n
		Snippet: driver.display.gprfMeasurement.spectrum.set_trace(value = TraceStruct()) \n
		Selects which traces are displayed on the 'Spectrum Analyzer' tab. \n
			:param value: see the help for TraceStruct structure arguments.
		"""
		self._core.io.write_struct('DISPlay:GPRF:MEASurement<Instance>:SPECtrum:TRACe', value)

	def clone(self) -> 'Spectrum':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spectrum(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
