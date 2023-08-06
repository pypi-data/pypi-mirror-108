from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bpass:
	"""Bpass commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpass", core, parent)

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Disable or enable filter for left SPDIF channel
			- Enable_Right: bool: OFF | ON Disable or enable filter for right SPDIF channel"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_bool('Enable_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Enable_Right: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.spdif.filterPy.bpass.get_enable() \n
		Enables or disables the variable bandpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:ENABle \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.bpass.set_enable(value = EnableStruct()) \n
		Enables or disables the variable bandpass filter in the SPDIF input path. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:ENABle', value)

	# noinspection PyTypeChecker
	class CfrequencyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Frequency_Left: float: Frequency for left SPDIF channel Unit: Hz
			- Frequency_Right: float: Frequency for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_Left'),
			ArgStruct.scalar_float('Frequency_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_Left: float = None
			self.Frequency_Right: float = None

	def get_cfrequency(self) -> CfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency \n
		Snippet: value: CfrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.bpass.get_cfrequency() \n
		Configures the center frequency of the variable bandpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for CfrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency?', self.__class__.CfrequencyStruct())

	def set_cfrequency(self, value: CfrequencyStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.bpass.set_cfrequency(value = CfrequencyStruct()) \n
		Configures the center frequency of the variable bandpass filter in the SPDIF input path. \n
			:param value: see the help for CfrequencyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency', value)

	# noinspection PyTypeChecker
	class BandwidthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Bandwidth_Left: float: Bandwidth for left SPDIF channel Unit: Hz
			- Bandwidth_Right: float: Bandwidth for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Bandwidth_Left'),
			ArgStruct.scalar_float('Bandwidth_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bandwidth_Left: float = None
			self.Bandwidth_Right: float = None

	def get_bandwidth(self) -> BandwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth \n
		Snippet: value: BandwidthStruct = driver.configure.afRf.measurement.spdif.filterPy.bpass.get_bandwidth() \n
		Configures the bandwidth of the variable bandpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for BandwidthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth?', self.__class__.BandwidthStruct())

	def set_bandwidth(self, value: BandwidthStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.bpass.set_bandwidth(value = BandwidthStruct()) \n
		Configures the bandwidth of the variable bandpass filter in the SPDIF input path. \n
			:param value: see the help for BandwidthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth', value)
