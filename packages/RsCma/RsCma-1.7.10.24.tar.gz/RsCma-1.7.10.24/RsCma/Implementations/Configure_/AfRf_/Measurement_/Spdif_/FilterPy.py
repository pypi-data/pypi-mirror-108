from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 11 total commands, 2 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	@property
	def bpass(self):
		"""bpass commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_bpass'):
			from .FilterPy_.Bpass import Bpass
			self._bpass = Bpass(self._core, self._base)
		return self._bpass

	@property
	def notch(self):
		"""notch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_notch'):
			from .FilterPy_.Notch import Notch
			self._notch = Notch(self._core, self._base)
		return self._notch

	# noinspection PyTypeChecker
	class LpassStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Filter_Left: enums.LowpassFilterExtended: OFF | F255 | F3K | F3K4 | F4K | F15K Left SPDIF channel
			- Filter_Right: enums.LowpassFilterExtended: OFF | F255 | F3K | F3K4 | F4K | F15K Right SPDIF channel OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.LowpassFilterExtended),
			ArgStruct.scalar_enum('Filter_Right', enums.LowpassFilterExtended)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.LowpassFilterExtended = None
			self.Filter_Right: enums.LowpassFilterExtended = None

	# noinspection PyTypeChecker
	def get_lpass(self) -> LpassStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs \n
		Snippet: value: LpassStruct = driver.configure.afRf.measurement.spdif.filterPy.get_lpass() \n
		Configures the lowpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for LpassStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs?', self.__class__.LpassStruct())

	def set_lpass(self, value: LpassStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_lpass(value = LpassStruct()) \n
		Configures the lowpass filter in the SPDIF input path. \n
			:param value: see the help for LpassStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs', value)

	# noinspection PyTypeChecker
	class HpassStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Filter_Left: enums.HighpassFilterExtended: OFF | F6 | F50 | F300 Left SPDIF channel OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
			- Filter_Right: enums.HighpassFilterExtended: OFF | F6 | F50 | F300 Right SPDIF channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.HighpassFilterExtended),
			ArgStruct.scalar_enum('Filter_Right', enums.HighpassFilterExtended)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.HighpassFilterExtended = None
			self.Filter_Right: enums.HighpassFilterExtended = None

	# noinspection PyTypeChecker
	def get_hpass(self) -> HpassStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs \n
		Snippet: value: HpassStruct = driver.configure.afRf.measurement.spdif.filterPy.get_hpass() \n
		Configures the highpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for HpassStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs?', self.__class__.HpassStruct())

	def set_hpass(self, value: HpassStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_hpass(value = HpassStruct()) \n
		Configures the highpass filter in the SPDIF input path. \n
			:param value: see the help for HpassStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs', value)

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dwidth_Left: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth, left channel
			- Drelative_Left: enums.Relative: RELative | CONStant Proportional to reference frequency or constant, left channel
			- Dwidth_Right: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth, right channel
			- Drelative_Right: enums.Relative: RELative | CONStant Proportional to reference frequency or constant, right channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth_Left', enums.PwrFilterType),
			ArgStruct.scalar_enum('Drelative_Left', enums.Relative),
			ArgStruct.scalar_enum('Dwidth_Right', enums.PwrFilterType),
			ArgStruct.scalar_enum('Drelative_Right', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth_Left: enums.PwrFilterType = None
			self.Drelative_Left: enums.Relative = None
			self.Dwidth_Right: enums.PwrFilterType = None
			self.Drelative_Right: enums.Relative = None

	# noinspection PyTypeChecker
	def get_dwidth(self) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.spdif.filterPy.get_dwidth() \n
		Configures the bandwidth of the distortion filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for DwidthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DWIDth?', self.__class__.DwidthStruct())

	def set_dwidth(self, value: DwidthStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_dwidth(value = DwidthStruct()) \n
		Configures the bandwidth of the distortion filter in the SPDIF input path. \n
			:param value: see the help for DwidthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DWIDth', value)

	# noinspection PyTypeChecker
	class WeightingStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Filter_Left: enums.WeightingFilter: OFF | AWEighting | CCITt | CMESsage Left SPDIF channel OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
			- Filter_Right: enums.WeightingFilter: OFF | AWEighting | CCITt | CMESsage Right SPDIF channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.WeightingFilter),
			ArgStruct.scalar_enum('Filter_Right', enums.WeightingFilter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.WeightingFilter = None
			self.Filter_Right: enums.WeightingFilter = None

	# noinspection PyTypeChecker
	def get_weighting(self) -> WeightingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting \n
		Snippet: value: WeightingStruct = driver.configure.afRf.measurement.spdif.filterPy.get_weighting() \n
		Configures the weighting filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for WeightingStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting?', self.__class__.WeightingStruct())

	def set_weighting(self, value: WeightingStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_weighting(value = WeightingStruct()) \n
		Configures the weighting filter in the SPDIF input path. \n
			:param value: see the help for WeightingStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting', value)

	# noinspection PyTypeChecker
	class DfrequencyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Distor_Freq_Left: float: Frequency for left SPDIF channel Unit: Hz
			- Distor_Freq_Right: float: Frequency for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Distor_Freq_Left'),
			ArgStruct.scalar_float('Distor_Freq_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Distor_Freq_Left: float = None
			self.Distor_Freq_Right: float = None

	def get_dfrequency(self) -> DfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency \n
		Snippet: value: DfrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.get_dfrequency() \n
		Configures the reference frequency for single-tone measurements via the SPDIF input path. \n
			:return: structure: for return value, see the help for DfrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency?', self.__class__.DfrequencyStruct())

	def set_dfrequency(self, value: DfrequencyStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_dfrequency(value = DfrequencyStruct()) \n
		Configures the reference frequency for single-tone measurements via the SPDIF input path. \n
			:param value: see the help for DfrequencyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency', value)

	# noinspection PyTypeChecker
	class RobustAutoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Automatic_Mode_Left: bool: OFF | ON
			- Automatic_Mode_Right: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Automatic_Mode_Left'),
			ArgStruct.scalar_bool('Automatic_Mode_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Automatic_Mode_Left: bool = None
			self.Automatic_Mode_Right: bool = None

	def get_robust_auto(self) -> RobustAutoStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto \n
		Snippet: value: RobustAutoStruct = driver.configure.afRf.measurement.spdif.filterPy.get_robust_auto() \n
		Enables or disables robust automatic mode for distortion signal filtering in the SPDIF input path. \n
			:return: structure: for return value, see the help for RobustAutoStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto?', self.__class__.RobustAutoStruct())

	def set_robust_auto(self, value: RobustAutoStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.set_robust_auto(value = RobustAutoStruct()) \n
		Enables or disables robust automatic mode for distortion signal filtering in the SPDIF input path. \n
			:param value: see the help for RobustAutoStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto', value)

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
