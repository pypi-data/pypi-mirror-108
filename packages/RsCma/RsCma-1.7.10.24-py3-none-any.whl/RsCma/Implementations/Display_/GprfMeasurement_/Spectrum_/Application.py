from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("application", core, parent)

	# noinspection PyTypeChecker
	class SelectStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Application: enums.SpecAnApp: FREQ | ZERO Show 'Frequency Sweep' subtab or 'Zero Span' subtab
			- Fullscreen: bool: OFF | ON OFF: show result diagram with default size ON: maximize result diagram"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Application', enums.SpecAnApp),
			ArgStruct.scalar_bool('Fullscreen')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Application: enums.SpecAnApp = None
			self.Fullscreen: bool = None

	# noinspection PyTypeChecker
	def get_select(self) -> SelectStruct:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect \n
		Snippet: value: SelectStruct = driver.display.gprfMeasurement.spectrum.application.get_select() \n
		Configures the display of the 'Spectrum Analyzer' tab. \n
			:return: structure: for return value, see the help for SelectStruct structure arguments.
		"""
		return self._core.io.query_struct('DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect?', self.__class__.SelectStruct())

	def set_select(self, value: SelectStruct) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect \n
		Snippet: driver.display.gprfMeasurement.spectrum.application.set_select(value = SelectStruct()) \n
		Configures the display of the 'Spectrum Analyzer' tab. \n
			:param value: see the help for SelectStruct structure arguments.
		"""
		self._core.io.write_struct('DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect', value)
